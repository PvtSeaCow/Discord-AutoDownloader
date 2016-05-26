import discord
import asyncio
import unicodedata

import json
import os
import requests

from sys import modules

client = discord.Client()

f = open('credentials.txt', 'r')
login_info = f.read().split(':')
f.close()

@client.async_event
async def on_ready():
    print('------')
    print('Auto Downloader\nBy Moe Sea Cow\nLogged in as ['+client.user.name+' (ID: "'+client.user.id+'")]')
    print('------')

@client.async_event
async def on_message(message):
    if (not message.channel.is_private) and ((message.embeds) or (message.attachments)) and (not message.channel.is_default):
        if 'nsfw' in message.channel.name or 'fap' in message.channel.name or 'lood' in message.channel.name or 'lewd' in message.channel.name or 'illow ' in str(message.server.name):
            name = str(message.server.name)+'\\'+str(message.channel.name)
        else:
            name = str(message.server.name)+'\\'+str(message.channel.name)+'\\'+str(message.author.name)
        if message.embeds:
            for pic in message.embeds:
                thing = str(pic['url']).split('/')
                try:
                    await download_file(str(pic['url']), name, str(thing[-1].split('.')[0]), str(thing[-1].split('.')[-1]))
                except:
                    pass
        elif message.attachments:
            for pic in message.attachments:
                thing = str(pic['url']).split('/')
                try:
                    await download_file(str(pic['url']), name, str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                except:
                    pass
        elif r_image.match(urls[0]):
            for pic in urls:
                thing = str(pic).split('/')
                try:
                    await download_file(str(pic), name, str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                except:
                    pass
        else:
            print('ERROR!! |'+str(pic['url'])+'|'+name+'|'+str(thing[-1].split('.')[-2])+'|'+str(thing[-1].split('.')[-1]))
    elif (message.channel.is_private) and (message.embeds or message.attachments):
        name = '@pms\\'+str(message.channel.user)
        if message.embeds:
            for pic in message.embeds:
                thing = str(pic['url']).split('/')
                try:
                    await download_file(str(pic['url']), name, str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                except:
                    pass
        elif message.attachments:
            for pic in message.attachments:
                thing = str(pic['url']).split('/')
                try:
                    await download_file(str(pic['url']), name, str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                except:
                    pass
        else:
            print('ERROR!! |'+str(pic['url'])+'|'+name+'|'+str(thing[-1].split('.')[-2])+'|'+str(thing[-1].split('.')[-1]))


async def download_file(url, path, file_name, file_type):
    if file_type == 'exe' or file_name == 'js':
        return
    if not os.path.exists('.\\pictures\\'+path):
        os.makedirs('.\\pictures\\'+path)
    headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
    }
    r = requests.get(url, headers=headers, stream=True)
    with open('.\\pictures\\'+path+'\\'+str(file_name)+'.'+str(file_type), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

client.run(login_info[0], login_info[1])