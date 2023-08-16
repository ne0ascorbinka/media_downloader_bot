# beside imports
import subprocess
import re
import os
import shutil

# pyrogram imports
from pyrogram import Client
from pyrogram.types import CallbackQuery

from logger import logger, Status
from credentials import BOT_USERNAME

# TODO: add path :3

def download_video_youtube(video_quality: str, video_link: str, path: str, vertical : bool = None):
    """quality: full_hd->1080, hd->720, fsd->480, sd->360"""
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

    if video_quality not in dic_of_quality.keys():
        command = f"yt-dlp -f 'ba' -x --audio-format mp3 {video_link}  -o '{path}/%(id)s.%(ext)s'" #TODO: make it multiplatofrmic
        os.system(command)
        return None

    if vertical:
        command = f'yt-dlp -f "bv*[ext=mp4][width={dic_of_quality[video_quality]}]+ba[ext=m4a]/b[ext=mp4]" "{video_link}" -o "{path}/%(title)s.%(ext)s"'
    else:
        command = f'yt-dlp -f "bv*[ext=mp4][height={dic_of_quality[video_quality]}]+ba[ext=m4a]/b[ext=mp4]" "{video_link}" -o "{path}/%(title)s.%(ext)s"'
    os.system(command)
    return None


def get_resolutions(url: str):
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

def youtube_download(client: Client, callback_query: CallbackQuery):
    video_quality = callback_query.data.split()[1]
    video_link = callback_query.data.split()[2]
    is_vertical = int(callback_query.data.split()[3])

    callback_query.message.edit(f"Downloading video with quality {video_quality}...")
    user_id = callback_query.message.chat.id
    try:
        #downloads_path = DOWNLOADS_PATH
       # path = os.path.join(downloads_path, str(user_id))
        folder_path = str(user_id)
        os.mkdir(folder_path)

        download_video_youtube(video_quality, video_link, folder_path, is_vertical)

        file_name = os.listdir(folder_path)[0]
        file_path = os.path.join(folder_path, file_name)

        logger.info(
            f"downloaded youtube link",
            extra={
                "id": callback_query.message.chat.id,
                "status": Status.SUCCESS})
        callback_query.message.edit("__Downloaded! Uploading...__")
        callback_query.message.reply_video(file_path, caption=f"__Downloaded via @{BOT_USERNAME}__")
        callback_query.message.delete()

        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            logger.error(f"Couldn't delete video file - {e}", extra={
                "id" : user_id,
                "status" : Status.FAILURE
            })

    except Exception as e:
        print(e)
        callback_query.message.edit(f"__Error happened during downloading :(__")
        logger.error(
            f"couldn't download YT video, following url caused the error - {callback_query.data}",
            extra={
            "id" : callback_query.message.chat.id,
            "status" : Status.FAILURE
            }
        )
        try:
            shutil.rmtree(folder_path)
        except Exception:
            logger.warn(f"couldn't delete folder path", extra={
            "id" : callback_query.message.chat.id,
            "status" : Status.FAILURE
            })
        #logger.warn(f"Following message content threw an exception above: {message}")

def main() -> None:
    url = "https://www.youtube.com/watch?v=quvgVDiRtNQ"
    resolutions, vertical = (get_resolutions(url))
    print(resolutions)
    download_video_youtube("1080p", url, vertical)

if __name__ == "__main__":
    main()