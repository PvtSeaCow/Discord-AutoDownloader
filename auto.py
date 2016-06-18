import pip
try:
    import discord
except:
    pip.main(['install', 'git+https://github.com/Rapptz/discord.py@async'])
    sleep(2)
    import discord
import asyncio
import unicodedata

import json
import os
import re
import subprocess
try:
    import requests
except :
    import pip
    pip.main(['install', 'requests'])
    import requests
try:
    import imgurpython
    from imgurpython import ImgurClient
except:
    pip.main(['install', 'imgurpython'])
    sleep(2)
    import imgurpython
    from imgurpython import ImgurClient

from sys import modules

client = discord.Client()

def setup():
    f = open("credentials.txt", 'w+')
    email = input('Email: ')
    password = input('Password: ')
    f.write(email+':'+password)
    f.close()

try:
    f = open('credentials.txt', 'r')
    login_info = f.read().split(':')
    f.close()
except:
    print('ERROR: \'credentials.txt\' not found!')
    setup()
    sleep(2)
    sys.exit(0)

try:
    f = open('imgur.txt', 'r')
    imgur_info = f.read().split(':')
    f.close()
    imgur = ImgurClient(imgur_info[0],imgur_info[0])
except:
    print('Register a imgur key at: https://api.imgur.com/oauth2/addclient')
    print('''Select 'OAuth2 without url' ''')
    f = open("imgur.txt", 'w+')
    ID = input('Client ID: ')
    Secret = input(' Client Secret: ')
    f.write(ID+':'+Secret)
    f.close()
    sleep(2)
    sys.exit(0)

@client.async_event
async def on_ready():
    subprocess.call('cls',shell=True)
    print('------')
    print('Auto Downloader (By Moe Sea Cow)\nCurrently logged in as ['+client.user.name+' (ID: "'+client.user.id+'")]')
    print('Number of Servers Connected: '+str(len(list(client.servers)))+'\nNumbers of DMs: '+str(len(list(client.private_channels))))
    print('------')
    await client.change_status(idle=True)


@client.async_event
async def on_message(message):
    imgurlink = re.findall("(https?)\:\/\/(?:i\.)?(www\.)?(?:m\.)?imgur\.com\/(gallery\/|a\/|r\/[a-z]+)?(?:\/)?([a-zA-Z0-9]+)(#[0-9]+)?(?:\.gifv)?", message.content)
    imgurmatch = re.match("(https?)\:\/\/(?:i\.)?(www\.)?(?:m\.)?imgur\.com\/(gallery\/|a\/|r\/[a-z]+)?(?:\/)?([a-zA-Z0-9]+)(#[0-9]+)?(?:\.gifv)?", message.content)
    try:
        if imgurmatch:
            try:
                for lnk in imgurlink:
                    if 'nsfw' in message.channel.name or 'fap' in message.channel.name or 'lood' in message.channel.name or 'lewd' in message.channel.name or 'illow ' in str(message.server.name):
                        name = str(message.server.name)+'\\'+str(message.channel.name)+'\\@imgur\\'+str(imgur.get_album(lnk[3]).id)
                    else:
                        name = str(message.server.name)+'\\'+str(message.channel.name)+'\\'+str(message.author.name)+'\\@imgur\\'+str(imgur.get_album(lnk[3]).id)
                    for pic in imgur.get_album_images(lnk[3]):
                        if pic.animated:
                            thing = str(pic.link).split('/')
                            await download_file(str(pic.webm), str(name), str(thing[-1].split('.')[-2]), 'webm')
                        else:
                            thing = str(pic.link).split('/')
                            await download_file(str(pic.link), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
            except:
                for lnk in imgurlink:
                    if 'nsfw' in message.channel.name or 'fap' in message.channel.name or 'lood' in message.channel.name or 'lewd' in message.channel.name or 'illow ' in str(message.server.name):
                        name = str(message.server.name)+'\\'+str(message.channel.name)+'\\@imgur\\'+str(imgur.get_image(lnk[3]).id)
                    else:
                        name = str(message.server.name)+'\\'+str(message.channel.name)+'\\'+str(message.author.name)+'\\@imgur\\'+str(imgur.get_image(lnk[3]).id)
                    pic = imgur.get_image(lnk[3])
                    if pic.animated:
                        thing = str(pic.link).split('/')
                        await download_file(str(pic.webm), str(name), str(thing[-1].split('.')[-2]), 'webm')
                    else:
                        thing = str(pic.link).split('/')
                        await download_file(str(pic.link), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
        elif (not message.channel.is_private) and ((message.embeds) or (message.attachments)) and (not imgurmatch):
            if 'nsfw' in message.channel.name or 'fap' in message.channel.name or 'lood' in message.channel.name or 'lewd' in message.channel.name or 'illow ' in str(message.server.name):
                name = str(message.server.name)+'\\'+str(message.channel.name)
            else:
                name = str(message.server.name)+'\\'+str(message.channel.name)+'\\'+str(message.author.name)
            if message.embeds:
                for pic in message.embeds:
                    thing = str(pic['url']).split('/')
                    try:
                        await download_file(str(pic['url']), str(name), str(thing[-1].split('.')[0]), str(thing[-1].split('.')[-1]))
                    except:
                        pass
            elif message.attachments:
                for pic in message.attachments:
                    thing = str(pic['url']).split('/')
                    try:
                        await download_file(str(pic['url']), (name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                    except:
                        pass
            elif r_image.match(urls[0]):
                for pic in urls:
                    thing = str(pic).split('/')
                    try:
                        await download_file(str(pic), (name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                    except:
                        pass
            else:
                print('ERROR!! |'+str(pic['url'])+'|'+name+'|'+str(thing[-1].split('.')[-2])+'|'+str(thing[-1].split('.')[-1]))
        elif (message.channel.is_private) and (message.embeds or message.attachments) and (not imgurmatch):
            name = '@pms\\'+str(message.channel.user)
            if message.embeds:
                for pic in message.embeds:
                    thing = str(pic['url']).split('/')
                    try:
                        await download_file(str(pic['url']), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                    except:
                        pass
            elif message.attachments:
                for pic in message.attachments:
                    thing = str(pic['url']).split('/')
                    try:
                        await download_file(str(pic['url']), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]))
                    except:
                        pass
            else:
                print('ERROR!! |'+str(pic['url'])+'|'+name+'|'+str(thing[-1].split('.')[-2])+'|'+str(thing[-1].split('.')[-1]))
    except Exception as e:
        raise
        print(message.server.name+': '+message.author.name+': '+message.content)


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