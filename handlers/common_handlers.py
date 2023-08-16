from typing import Union
from functions import dynamic_data_filter
from pyrogram import Client, filters
from pyrogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from credentials import BOT_NAME, chat_ids, CHAT_IDS_PATH
from logger import logger, Status

async def show_start(client: Client, update: Union[Message, CallbackQuery]):
    username = None
    if isinstance(update, CallbackQuery):
        username = update.message.chat.first_name
    else:
        username = update.chat.first_name
    start_message = f"""Hello, **{username}**!\nWelcome to the {BOT_NAME}! This bot can download:
1. Video from **TikTok**.
2. Tracks, playlists, albums from **Spotify**.
3. Posts from **Instagram**."""

    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("press me", callback_data="data")]])

    if isinstance(update, Message):
        await update.reply(start_message, reply_markup=markup)
    else:
        message = update.message
        await message.edit(start_message, reply_markup=markup)

async def button_handler(client: Client, callback_query: CallbackQuery):

    button = InlineKeyboardButton("Go back", callback_data="user_start")
    markup = InlineKeyboardMarkup([[button]])

    await callback_query.message.edit("You've just pressed some button\n\nYou can go back now", reply_markup=markup)

async def start_handler(client: Client, message: Message):
    """
    Replies to start command with start message
    """
    if message.chat.id not in chat_ids:
        logger.info(f"user{message.chat.first_name} joined the bot", extra={
            "id": message.chat.id, "status": Status.SUCCESS})
        chat_ids.add(message.chat.id)
        with open(CHAT_IDS_PATH, 'a') as f:
            f.write(str(message.chat.id))
            f.write('\n')

    start_message = f"""Hello, **{message.chat.first_name}**!
\nWelcome to the {BOT_NAME}! This bot can download:
1. Videos from **TikTok**.
2. Tracks, playlists, albums from **Spotify**.
3. Videos from **YouTube**."""
    button1 = InlineKeyboardButton("Button1 :/", callback_data="data1")
    button2 = InlineKeyboardButton("Button2 :/", callback_data="data2")
    button3 = InlineKeyboardButton("Button3 :/", callback_data="data3")
    button4 = InlineKeyboardButton("Button4 :/", callback_data="data4")
    markup = InlineKeyboardMarkup([[button1, button2], [button3, button4]])

    await message.reply_text(start_message, reply_markup=markup)

async def link_handler(client: Client, message: Message):
    await message.reply("Unsupported type of link :(")
    link = message.text
    user_id = message.chat.id
    logger.info(f"Unsupported link - {link}", extra={
        "id" : user_id,
        "status" : Status.UNKNOWN
    })

    # # print(message)
    # try:
    #     logger.debug(f"trying")
    #     audio_id = str(random.randint(100000, 999999))
    #     audio_path = os.path.join(".", "audio")

    #     logger.info(f"url [{message.text}]")
    #     logger.info(f"audio_path [{audio_path}]")
    #     logger.info(f"audio_id [{audio_id}]")
    #     await message.reply("... was found, downloading...")

    #     await message.reply("... downloaded. Sending...")

    #     logger.debug(f"sending {audio_id}")

    #     # await message.reply_video(os.path.join(audio_path, audio_id))

    #     logger.debug(f"done, removing video [{audio_id}]")

    #     os.remove(os.path.join(audio_path, audio_id))
    #     logger.debug("workflow finished SUCCESS")

    # except Exception as e:
    #     logger.error(f"following exception caught\n{e}\n")
    #     logger.debug(str(message))
    #     logger.debug(f"sending error message to user")
    #     await message.reply("Not valid link or error")
    #     logger.debug("workflow finished FAIL")

async def message_handler(client: Client, message: Message):
    logger.debug(f"user sent message: {message.link}")
    await message.reply("Please send me a link")

def set_common_handlers(app: Client):
    app.add_handler(MessageHandler(show_start, filters.command("start")))
    app.add_handler(CallbackQueryHandler(show_start, dynamic_data_filter(["back", "user_start"])))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(MessageHandler(start_handler, filters.private & filters.command("start")))

    app.add_handler(MessageHandler(link_handler, filters.regex("(https?://)?(www\.)?\w+\.[a-z]+") & filters.private))

    app.add_handler(MessageHandler(message_handler, filters.text & filters.private))