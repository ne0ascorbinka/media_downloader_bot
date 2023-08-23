from pyrogram import Client
from pyrogram.types import InputMediaAudio
import os
from .base_downloader import BaseDownloader
from config import config

class SpotifyDownloader(BaseDownloader):
    def __init__(self, client: Client, id: int, url: str) -> None:
        super().__init__(client, id, url)
    
    def download(self) -> None:
        print("trying to dl spotify")
        sent_message = self.client.send_message(self.id, "__Downloading...__")
        self.sent_message = sent_message
        os.chdir(f"{self.folder_path}") #step into downloading folder
        try:
            os.system(f'spotdl "{self.url}"')
        except:
            print(self.url)
        os.chdir("..") # and step out
    
    def _upload(self) -> None:
        sent_message = self.sent_message
        sent_message.edit("__Downloaded! Uploading...__")
        # Отримання списку файлів у папці
        files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]

        # Якщо є лише один файл
        if len(files) == 1:
            self.client.send_audio(chat_id=self.id, audio=files[0], caption=f"__via @{config.BOT_USERNAME}__")
        # Якщо є декілька файлів
        elif len(files) > 1:
            for i in range(0, len(files), 10):
                media_group = [InputMediaAudio(media=file) for file in files[i:i+10]]
                self.client.send_media_group(chat_id=self.id, media=media_group)
        sent_message.delete()
        