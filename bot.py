# pyrogram imports
from pyrogram import Client

from logger import logger
from functions import *
from handlers import admin_handlers, common_handlers, inline_handlers, downloading_handlers
from credentials import (chat_ids, BOT_NAME, API_ID, API_HASH, BOT_TOKEN)

# Client init
def get_client():
    return Client(BOT_NAME,
                  api_id=API_ID,
                  api_hash=API_HASH,
                  bot_token=BOT_TOKEN)

app = get_client()
greeter = get_client()
# TODO : Maybe it is a good idea to create messages in global, or even
# take them from some JSON

async def notify():
    async with greeter:
        for id in chat_ids:
            await greeter.send_message(id, "Bot has been started again!")



async def notify_me():
    async with greeter:
        #user = "hustly" # meh #bruh
        user = "neascorbinka"
        await greeter.send_message(user, "started!")

def main():
    try:
        with open("chat_ids.txt", "r") as f:
            for line in f.readlines():
                chat_ids.add(int(line))
    except FileNotFoundError:
        pass

    downloading_handlers.set_downloading_handlers(app)
    admin_handlers.set_admin_handlers(app)
    common_handlers.set_common_handlers(app)
    # inline_handlers.set_inline_handlers(app)

    logger.debug("started")
    print("started")
    greeter.run(notify_me())

    app.run()

if __name__ == "__main__":
    main()
