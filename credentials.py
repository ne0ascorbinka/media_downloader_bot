"""
Credentials module in root folder. It has use in porject already (hooray)
"""

import json
from concurrent.futures import ThreadPoolExecutor

with open("config.json") as file:
    data = json.load(file)

BOT_NAME = data["bot_name"]
API_ID = data["api_id"]
API_HASH = data["api_hash"]
BOT_TOKEN = data["bot_token"]
vip_ids = {1172987388, 528705708, 3} #???
ROOT_FOLDER_PATH = "/home/test/bot/Typo_boty/new/bot" #WTF
CHAT_IDS_PATH = data["chat_ids_path"]
BOT_USERNAME = data["bot_username"]
DOWNLOADS_PATH = data["downloads_path"]
ADMINS = data["allowed_users"]

chat_ids = set()
vip_pool_executor = ThreadPoolExecutor(max_workers=1)
other_pool_executor = ThreadPoolExecutor(max_workers=1)

import re

SPOTIFY_LINK_PATTERN = re.compile(
    r'^https?://(?:[a-z]+\.)?spotify\.(?:com|[a-z]{2,3})'
    r'(/((?:track|playlist|album|artist|show|episode)/)?)?'
)
TIKTOK_LINK_PATTERN = "^(?:https?:\\/\\/)?(?:www\\.)?(?:tiktok\\.com\\/@(?:[a-zA-Z0-9_\\-]+\\.)?\
(?:[a-zA-Z0-9_\\-]+)\\/video\\/([a-zA-Z0-9_\\-]+)(?:\\?|\\&|\\#|$)|vm\\.tiktok\\.com\\/([a-zA-Z0-9_\\-]+))\\S*$"
INSTAGRAM_LINK_PATTERN = "^(?:https?:\\/\\/)?(?:www\\.)?instagram\\.com\\/(?:[a-zA-Z0-9_\\-]+\\/)?\
(?:p|reel|tv)\\/([a-zA-Z0-9_\\-]+)(?:\\/.*)?$"
YOUTUBE_LINK_PATTERN = "^(?:https?:\\/\\/)?(?:www\\.)?(?:m\\.)?youtube\\.com\\/watch\\?v=([a-zA-Z0-9_-]{11})(?:\\S+)?\
|(?:https?:\\/\\/)?(?:www\\.)?youtu\\.be\\/([a-zA-Z0-9_-]{11})(?:\\S+)?$"
SOUNDCLOUD_LINK_PATTER = "https?://(?:www\\.)?soundcloud\\.com/([^\\s/]+)/([^\\s/?\\.]+)$"

CONTENT_TYPE_MAP = {
    'track': 'song',
    'playlist': 'playlist',
    'album': 'album',
    'artist': 'artist',
    'show': 'podcast show',
    'episode': 'podcast episode'
}