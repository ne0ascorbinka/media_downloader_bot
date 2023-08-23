"""Module with helper classes"""

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import pool_executor
from core import BaseDownloader, SpotifyDownloader, TiktokDownloader, YouTubeDownloader
import re
import subprocess
import asyncio

class BaseHandler:
    def __init__(self, client: Client, id: int, url: str) -> None:
        self.client = client
        self.id = id
        self.url = url

    def handle(self) -> None:
        # print(f"Handling url {self.url} from chat {self.id}")
        downloader = BaseDownloader(self.client, self.id, self.url)
        pool_executor.submit(downloader.start)

class SpotifyHandler(BaseHandler):
    def __init__(self, client: Client, id: int, url: str) -> None:
        super().__init__(client, id, url)
    
    def handle(self) -> None:
        print("trying to handle spotify")
        downloader = SpotifyDownloader(self.client, self.id, self.url)
        pool_executor.submit(downloader.start)

class TiktokHandler(BaseHandler):
    def __init__(self, client: Client, id: int, url: str) -> None:
        super().__init__(client, id, url)
    
    def handle(self) -> None:
        print("trying to handler tiktok")
        tiktok_downloader = TiktokDownloader(self.client, self.id, self.url)
        pool_executor.submit(tiktok_downloader.start)

class YouTubeHandler(BaseHandler):
    def __init__(self, client: Client, id: int, url: str) -> None:
        super().__init__(client, id, url)
    
    def handle(self) -> None:
        youtube_downloader = YouTubeDownloader(self.client, self.id, self.url)
        pool_executor.submit(youtube_downloader.ask_resolution)


class HandlerFactory:

    def __init__(self, url: str) -> None:
        self.url = url

    @staticmethod
    def create_handler(client: Client, id: int, url: str):
        SPOTIFY_URL_PATTER = re.compile("https:\/\/open\.spotify\.com\/(track|album|playlist)\/[a-zA-Z0-9]+")
        TIKTOK_URL_PATTERN = re.compile("https:\/\/(www\.tiktok\.com\/@[\w.-]+\/video\/\d+|vm\.tiktok\.com\/[a-zA-Z0-9]+)\/?")
        YOUTUBE_URL_PATTERN = re.compile("https?:\/\/(?:www\.)?(?:youtube\.com\/(?:watch\?v=|channel\/|user\/)|youtu\.be\/)[a-zA-Z0-9_-]+")
        if re.match(SPOTIFY_URL_PATTER, url):
            print("creating spotH")
            return SpotifyHandler(client, id, url)
        elif re.match(TIKTOK_URL_PATTERN, url):
            print("creating ttH")
            return TiktokHandler(client, id, url)
        elif re.match(YOUTUBE_URL_PATTERN, url):
            print("matched YT regex")
            return YouTubeHandler(client, id, url)
        return BaseHandler(client, id, url)