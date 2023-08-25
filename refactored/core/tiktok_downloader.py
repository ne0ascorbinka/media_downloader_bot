from pyrogram import Client
import os
import requests
import re
import time
from .base_downloader import BaseDownloader
from config import config

class TiktokDownloader(BaseDownloader):
    def __init__(self, client: Client, id: int, url: str) -> None:
        super().__init__(client, id, url)
    
    def download(self) -> None:
        self.sent_message = self.client.send_message(self.id, "__Downloading...__")

        link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', self.url)[0]
        link = link.split("?")[0]

        url = "https://tiktok82.p.rapidapi.com/getDownloadVideoWithoutWatermark"

        querystring = {"video_url" : link}

        headers = {
            "X-RapidAPI-Key": "685f6e97c3mshe1b81cdc5fd9189p1975ecjsna5d45b82df8a",
            "X-RapidAPI-Host": "tiktok82.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        # print(response.json())
        download_url = response.json()["video_url"]

        directory = self.folder_path
        filename = str(int(time.time())) + '.mp4'
        content_path = os.path.join(".", directory, filename)
        self.content_path = content_path
            
        with requests.get(download_url, timeout=(50, 10000), stream=True) as response:
            response.raise_for_status()
            with open(content_path, 'wb') as f:
                chunk_size = 1048576
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
    
    def _upload(self) -> None:
        sent_message = self.sent_message
        sent_message.edit(f"__Downloaded! Uploading...__")
        self.client.send_video(self.id, self.content_path, caption=f"__via @{config.BOT_USERNAME}__")
        sent_message.delete()
        

