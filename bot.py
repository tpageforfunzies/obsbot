# pip install discord.py and dotenv

import discord
import requests
import os
import json
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER_URL = os.getenv('SERVER_URL')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
APPROVAL_EMOJIS = json.loads(os.getenv('APPROVAL_EMOJIS'))
APPROVER_ROLES = json.loads(os.getenv('APPROVER_ROLES'))

client = discord.Client()


# HAVE TO CHANGE THE PUBLIC IP OF THE HOST IN THE ENV FILE AFTER EVERY OFF/ON

# FLOW
# on reaction (raw_reaction_add handler below) to image post 
# in submission channel with approval emoji by users with approver role
# collect the attachment url in the post
# send it to web server to download

@client.event
async def on_ready():
    print('We have logged into {0.guilds[0]} as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(raw_reaction):
    # first check if its a reaction in the right channel from the right people with the right emojis
    # if not, bail
    if not is_valid_event(raw_reaction):
        print('we dont care')
        return   
    
    # its the right stuff, is it a reaction to a picture?
    # if not, bail
    message_id = raw_reaction.message_id
    message = await get_message_by_id(message_id)
    if not message_has_attachment(message):
        print('no image attachment: we dont care')
        return
    
    # its a proper reaction to an image
    # grab url and send it to the server
    url = get_attachment_url(message)
    print(url)
    send_url_to_server(url)

@client.event
async def on_message(message):
    if not is_submission_channel(message.channel.id) or not is_approver(message.author):
        print('still dont care')
        return
    if message.content.startswith('!flush'):
        print('they said flush')
        flush_server_image_queue()
        # probably some success/fail return from server here
        return
    if message.content.startswith('!toggle'):
        print('they said toggle')
        toggle_stream_source()
        # probably some success/fail return from streamlabs here
        return


def is_valid_event(raw_reaction):
    # check for all the validation early for exit
    user = raw_reaction.member
    reaction = raw_reaction.emoji
    message_id = raw_reaction.message_id
    channel_id = raw_reaction.channel_id
    print('{} added reaction {} to message id {} in channel {}'.format(user, reaction, message_id, channel_id))
    if not is_submission_channel(channel_id):
        print('wrong channel')
        return False
    if not is_approver(user):
        print('not an approver')
        return False
    if not is_approval_emoji(reaction):
        print('wrong emoji')
        return False
    return True

def send_url_to_server(url):
    try:
        response = requests.post('http://{}/addimage'.format(SERVER_URL), data = {'image_url':url})
        print(response.text)
        print(response)
    except:
        print('something broke')
        raise

def flush_server_image_queue():
    # will call an endpoint to empty server queue
    # not implemented on server yet
    try:
        response = requests.post('http://{}/flushqueue'.format(SERVER_URL), data = {'hehe':'supersecretpasswordonlythebotknows'})
        print(response.text)
        print(response)
    except:
        print('something broke')
        raise


def toggle_stream_source():
    # if stream source on -> toggle off, etc
    # will prob need some kind of api key for obs' streamlabs
    print('toggle_stream_source')

def is_approver(user):
    # check if user reacting to image has the appropriate role
    # print(user.roles)
    for role in user.roles:
        if role.name in APPROVER_ROLES:
            return True
    return False

def is_approval_emoji(emoji):
    # check if the reaction was an approval emoji, for quick exit of handler
    # this will be done by getting the hash of the emoji, im not abuot to try to copy and paste emojis around
    emoji_name = emoji.name
    if emoji_name in APPROVAL_EMOJIS:
        return True
    return False

def is_submission_channel(channel_id):
    # check that message was posted in submission channel
    # can't tell bot to only listen on submission channel so
    # we have to manually remove its permissions in each other channel in the discord (which we want to, will reduce bot usage)
    # so until then, this can block processing the rest
    if channel_id == CHANNEL_ID:
        return True
    return False

def message_has_attachment(message):
    if message.attachments:
        return True
    return False

def get_attachment_url(message):
    return message.attachments[0].url


async def get_message_by_id(message_id):
    # to make the bot be able to handle messages that were sent before
    # it was turned on, we use the raw_reaction which gives us partial data
    # have to get specific message from that info (id)
    for channel in client.get_all_channels():
        try:
            msg = await channel.fetch_message(message_id)
        except:
            continue
    return msg


client.run(TOKEN)
