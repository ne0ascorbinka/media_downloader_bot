from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message
from handlers import HandlerRegistry
from logs.logger import logger

class RegularHandlers(HandlerRegistry):
    def __init__(self, client: Client):
        super().__init__(client)
    
    def register_handlers(self):
        logger.debug("registring handlers")
        client = self.client

        client.add_handler(MessageHandler(self.start_command, filters.command("start")))
        client.add_handler(CallbackQueryHandler(self.start_command, filters.command("start")))
        client.add_handler(MessageHandler(RegularHandlers.message_handler, filters.text))

    @staticmethod
    async def start_command(client: Client, message: Message):
        await message.reply_text("Hello!")
    
    @staticmethod
    async def message_handler(client: Client, message: Message):
        await message.reply("Send me a link")
