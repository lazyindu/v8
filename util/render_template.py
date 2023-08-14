#LazyDev
from info import *
from lazybot import StreamBot
from util.custom_dl import TGCustomYield
from util.file_size import human_size
import urllib.parse
import secrets
import mimetypes
import aiofiles
import logging
import aiohttp
from database.ia_filterdb import  get_file_details

async def fetch_properties(file_id):
    # file_id = await StreamBot.get_messages(LOG_CHANNEL, message_id)
    file_id = await get_file_details(file_id)
    file_properties = await TGCustomYield().generate_file_properties(file_id)
    file_name = file_properties.file_name if file_properties.file_name \
        else f"{secrets.token_hex(2)}.jpeg"
    mime_type = file_properties.mime_type if file_properties.mime_type \
        else f"{mimetypes.guess_type(file_name)}"
    return file_name, mime_type


async def render_page(file_id):
    file_name, mime_type = await fetch_properties(file_id)
    src = urllib.parse.urljoin(URL, str(file_id))
    audio_formats = ['audio/mpeg', 'audio/mp4', 'audio/x-mpegurl', 'audio/vnd.wav']
    video_formats = ['video/mp4', 'video/avi', 'video/ogg', 'video/h264', 'video/h265', 'video/x-matroska']
    try:
        if mime_type.lower() in video_formats:
            async with aiofiles.open('template/req.html') as r:
                heading = 'Watch {}'.format(file_name)
                tag = mime_type.split('/')[0].strip()
                html = (await r.read()).replace('tag', tag) % (heading, file_name, src)
        elif mime_type.lower() in audio_formats:
            async with aiofiles.open('template/req.html') as r:
                heading = 'Listen {}'.format(file_name)
                tag = mime_type.split('/')[0].strip()
                html = (await r.read()).replace('tag', tag) % (heading, file_name, src)
        else:
            async with aiofiles.open('template/dl.html') as r:
                async with aiohttp.ClientSession() as s:
                    async with s.get(src) as u:
                        file_size = human_size(u.headers.get('Content-Length'))
                        html = (await r.read()) % (heading, file_name, src, file_size)
    except Exception as e:
        # Print or log the error for debugging
        print("Error:", e)
        html = "<p>Error occurred while rendering the page</p>"
    return html
