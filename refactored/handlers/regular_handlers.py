from pyrogram import Client, filters
from .handler_registry import HandlerRegistry
from logs.logger import logger

class RegularHandlers(HandlerRegistry):
    def __init__(self, client: Client):
        super().__init__(client)
    
    def register_handlers(self):
        logger.debug("registring handlers")
        client = self.client

        client.add_handler(self.start_command, filters.command("start"))

    async def start_command(client, message):
        logger.debug("received start command")
        await message.reply_text("Hello!")
