from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import re
import subprocess
from .base_downloader import BaseDownloader
from config import config
import traceback
import os

class YouTubeDownloader(BaseDownloader):
    def __init__(self, client: Client, id: int, url: str, callback_query: CallbackQuery = None) -> None:
        super().__init__(client, id, url)
        self.callback_query = callback_query
    
    def download(self) -> None:
        dic_of_quality = {
        "1080p": 1080,
        "1080p60": 1080,
        "720p": 720,
        "720p60": 720,
        "480p": 480,
        "480p60": 480,
        "360p": 360,
        "360p60": 360,
        "240p60":240,
        "240p":240,
        "144p60":144,
        "144p":144
        }

        message = self.callback_query.message
        message.edit("__Downloading...__")

        url = self.url
        video_quality = self.get_video_quality()
        path = self.folder_path

        if video_quality not in dic_of_quality.keys():
            command = f"yt-dlp -f 'ba' -x --audio-format mp3 {url}  -o '{path}/%(id)s.%(ext)s'" #TODO: make it multiplatofrmic
            os.system(command)
            return None

        if self.video_is_vertical():
            command = f'yt-dlp -f "bv*[ext=mp4][width={dic_of_quality[video_quality]}]+ba[ext=m4a]/b[ext=mp4]" "{url}" -o "{path}/%(title)s.%(ext)s"'
        else:
            command = f'yt-dlp -f "bv*[ext=mp4][height={dic_of_quality[video_quality]}]+ba[ext=m4a]/b[ext=mp4]" "{url}" -o "{path}/%(title)s.%(ext)s"'
        os.system(command)
        return None
    
    def _upload(self) -> None:
        folder_path = self.folder_path

        file_name = os.listdir(folder_path)[0]
        file_path = os.path.join(folder_path, file_name)

        message = self.callback_query.message

        message.edit("__Downloaded! Uploading...__")
        
        if file_name.endswith(".mp4"):
            self.client.send_video(self.id, video=file_path, caption=f"__via @{config.BOT_USERNAME}__")
        else:
            self.client.send_audio(self.id, audio=file_path, caption=f"__via @{config.BOT_USERNAME}__")
        
        message.delete()



    def get_video_quality(self) -> str:
        video_quality = self.callback_query.data.split()[1]
        return video_quality
    
    def video_is_vertical(self) -> bool:
        is_vertical = int(self.callback_query.data.split()[3])
        return bool(is_vertical)

    def ask_resolution(self):
        url = self.url

        resolutions, is_vertical = self.get_resolutions(url)
        
        markup = InlineKeyboardMarkup(
            [
            [ InlineKeyboardButton(f"{resolution} | {resolutions[resolution]}",
                                callback_data=f"dlYT {resolution} {url} {int(is_vertical)}") ]
                for resolution in resolutions.keys()
            ]
        )
        self.client.send_message(self.id, "Choose quality:", reply_markup=markup)

    def get_resolutions(self, url: str):
        vertical = 0
        # Run the yt-dlp command and capture its output as a byte string
        result = subprocess.run(
            ["yt-dlp", "--list-formats", url], capture_output=True)

        # Convert the byte string to a regular string and split it into lines
        output_lines = result.stdout.decode().splitlines()
        if ("720x1280" in str(output_lines) or "144x256" in str(output_lines) or "360x640" in str(output_lines) ):
            vertical = 1

        # Iterate over the lines and extract the resolution information
        resolutions = dict()
        for line in output_lines:
            if "video only" in line:
                # Extract the resolution information from the line
                parts = line.split()
                res = parts[-2]
                size = parts[5]
                if "1080" in res or "720" in res or "420" in res or "360" in res or "240" in res:
                    if re.sub("\\,", "", res) not in resolutions:
                        resolutions[re.sub("\\,", "", res)] = size

        # Print the list of available resolutions
        for line in output_lines:
            if "audio only" in line and "m4a" in line and "medium" in line:
                size_of_audio = (line.split()[6])
        resolutions["Audio only"] = size_of_audio if size_of_audio else "unknown"

        return resolutions, vertical