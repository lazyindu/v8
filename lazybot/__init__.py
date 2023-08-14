# Thank You For subscribing my Yt @LazyDeveloper
from pyrogram import Client
from info import *

StreamBot = Client(
    session_name='Web Streamer',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=SLEEP_THRESHOLD,
    workers=WORKERS
)
