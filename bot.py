# pip install discord.py and dotenv

import discord
import os
from dotenv import load_dotenv
from pprint import pprint

CHANNEL_ID = 752892962748498024
APPROVAL_EMOJIS = [
    '🍕',
] 
APPROVER_ROLES = [
    'approver'
]

client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')

# FLOW
# on reaction to image post in submission channel with approval emoji by users with approver role
# collect the attachment in the post
# send it to web server

@client.event
async def on_ready():
    print('We have logged into {0.guilds[0]} as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(raw_reaction):
    user = raw_reaction.member
    reaction = raw_reaction.emoji
    message = raw_reaction.message_id
    channel_id = raw_reaction.channel_id
    print('{} added reaction {} to message id {}'.format(user, reaction, message))
    if not is_submission_channel(channel_id):
        print('channel id {} is not the submission channel, skipping'.format(channel_id))
        return
    
    if is_submission_channel(channel_id):
        print('channel id {} is the submission channel'.format(channel_id))
    if is_approver(user):
        print('{} is an approver'.format(user))
    if is_approval_emoji(reaction):
        print('{} is an approval emoji'.format(reaction))
    
@client.event
async def on_message(message):
    print('got message')
    # pprint(message)
    if message.attachments:
        print(message.attachments)
        print(message.attachments[0])
    print(message.content)
    print(message.author)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

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
    # print(emoji_name)
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

client.run(TOKEN)