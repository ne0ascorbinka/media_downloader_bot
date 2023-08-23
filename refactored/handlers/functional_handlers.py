from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery
from handlers import HandlerRegistry
from utils import BaseHandler, HandlerFactory
import re
from core import YouTubeDownloader
from config import pool_executor


class LinkHandlers(HandlerRegistry):
    URL_regex = "(https?://)?(www\.)?\w+\.[a-z]+"

    def __init__(self, client: Client):
        super().__init__(client)
    
    def register_handlers(self):
        client = self.client

        regex = re.compile(LinkHandlers.URL_regex)
        client.add_handler(MessageHandler(LinkHandlers.url_handler, filters.regex(regex)))
        client.add_handler(CallbackQueryHandler(LinkHandlers.youtube_callback_handler, filters.regex("dlYT.+")))

    @staticmethod
    async def url_handler(client: Client, message: Message):
        id = message.chat.id # chat ID
        url = message.text # TODO: maybe extract urls from messages
        print("trying to handle")
        HandlerFactory.create_handler(client, id, url).handle()
    
    @staticmethod
    async def youtube_callback_handler(client: Client, callback_query: CallbackQuery):
        print(callback_query.data)
        id = callback_query.message.chat.id
        url = callback_query.data.split()[2]
        youtube_downloader = YouTubeDownloader(client, id, url, callback_query)
        pool_executor.submit(youtube_downloader.start)