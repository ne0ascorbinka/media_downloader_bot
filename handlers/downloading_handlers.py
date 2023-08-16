# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery)
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from logger import logger, Status
from youtube.youtube_module import *
from spotify import spotify
from tiktok import tiktok
from credentials import (SPOTIFY_LINK_PATTERN, other_pool_executor, vip_ids,
                         vip_pool_executor, TIKTOK_LINK_PATTERN, YOUTUBE_LINK_PATTERN, SOUNDCLOUD_LINK_PATTER, INSTAGRAM_LINK_PATTERN)


async def tiktok_handler(client: Client, message: Message):
    sent = await message.reply(text='__Downloading...__',
                               parse_mode=ParseMode.MARKDOWN)
    id = message.from_user.id
    pool_executor = vip_pool_executor if id in vip_ids else other_pool_executor # TODO: we should stop using spotify credentials module
    pool_executor.submit(tiktok.tiktok_download, client, message, sent)

async def spotify_handler(client: Client, message: Message):
    sent = await message.reply("__Downloading...__")
    link = message.text
    id = message.from_user.id

    pool_executor = (other_pool_executor, vip_pool_executor)[id in vip_ids]
    pool_executor.submit(
        test_spotify.spotify_downloader,
        client,
        id,
        link,
        sent
    )

async def youtube_link_handler(client: Client, message: Message):
    url = message.text
    resolutions, is_vertical = get_resolutions(url)
    
    markup = InlineKeyboardMarkup(
        [
        [ InlineKeyboardButton(f"{resolution} | {resolutions[resolution]}",
                              callback_data=f"dlYT {resolution} {url} {int(is_vertical)}") ]
            for resolution in resolutions.keys()
        ]
    )
    await message.reply("Choose quality:", reply_markup=markup)

async def youtube_handler(client: Client, callback_query: CallbackQuery):
    id = callback_query.message.chat.id
    pool_executor = vip_pool_executor if id in vip_ids else other_pool_executor
    pool_executor.submit(youtube_download, client, callback_query)

def set_downloading_handlers(app: Client):
    app.add_handler(MessageHandler(tiktok_handler, filters.regex(TIKTOK_LINK_PATTERN)))
    app.add_handler(MessageHandler(spotify_handler, filters.regex(SPOTIFY_LINK_PATTERN)))

    app.add_handler(MessageHandler(youtube_link_handler, filters.regex(YOUTUBE_LINK_PATTERN)))
    app.add_handler(CallbackQueryHandler(youtube_handler, filters.regex(r"dlYT .+")))
