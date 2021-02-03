# pip install discord.py and dotenv

import discord
import os
from dotenv import load_dotenv
from pprint import pprint

client = discord.Client()

load_dotenv()
TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(raw_reaction):
    user = raw_reaction.member
    reaction = raw_reaction.emoji.name
    message = raw_reaction.message_id
    print('{} added reaction {} to message id {}'.format(user, reaction, message))
    
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

client.run(TOKEN)