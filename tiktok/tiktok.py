"""
Tiktok module that actually needs refactoring
"""
# beside imports
import os
import requests
import re
import shutil
import time

# pyrogram imports
from pyrogram import Client
from pyrogram.types import (
    Message)
from pyrogram.enums import ParseMode

from logger import logger, Status
from credentials import BOT_USERNAME

def tiktok_download(client: Client, message: Message, sent: Message):
    try:
        link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.text)[0]
        logger.debug(
            f"found link {link}")
        link = link.split("?")[0]

        params = {
            "link": link
        }
        headers = {
            'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
            'x-rapidapi-key': "f9d65af755msh3c8cac23b52a5eep108a33jsnbf7de971bb72"
        }

        # Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
        # Using the default one can stop working any moment

        api = f"https://tiktok-info.p.rapidapi.com/dl/"
        r = requests.get(api, params=params, headers=headers).json()[
            'videoLinks']['download']
        directory = str(round(time.time()))
        filename = str(int(time.time())) + '.mp4'
        os.mkdir(directory)
        
            
        with requests.get(r, timeout=(50, 10000), stream=True) as r:
            r.raise_for_status()
            with open(f'./{directory}/{filename}', 'wb') as f:
                chunk_size = 1048576
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        # why can't we use only id when it is needed?
        sent.edit(f"__Downloaded! Uploading...__")
        # logger.info(
        # f"downloaded {link}",
        # extra={
        #     "id": message.chat.id,
        #     "status": Status.UNKNOWN})
        # why reply_document? ;
        # no idea, but reply_document works
        message.reply_video(video=f"./{directory}/{filename}",
                            caption=f"__Downloaded via @{BOT_USERNAME}__")
        
        # message.reply_document(document=f"./{directory}/{filename}",
        #                         file_name=f"{directory}",
        #                         caption=f"__Downloaded via @{BOT_USERNAME}__",
        #                         parse_mode=ParseMode.MARKDOWN)
                              
        sent.delete()
        try:
            shutil.rmtree(directory)
        except BaseException as e:
            logger.warn("Couldn't delete directory file")
        logger.info(
        f"handled tiktok link",
        extra={
            "id": message.chat.id,
            "status": Status.SUCCESS})
    except Exception as e:
        logger.error(str(e), extra={
            "id" : id,
            "status" : Status.FAILURE
        })
        logger.warn(f"Following message content threw an exception above: {message}")