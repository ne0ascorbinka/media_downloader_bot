"""
Credentials module in spotify folder
"""

bot_name = "YoutubeDownloaderBot"
api_id = 19977182
api_hash = "17090836bf8a86617ed5739248226128"
bot_token = "5953742547:AAHuRX5vj2os1UMngyXKguLI9zfaWp66P38"
vip_ids = {1172987388, 528705708, 3}
ROOT_FOLDER_PATH = "/home/test/bot/test/test_env/"

import re

SPOTIFY_LINK_PATTERN = re.compile(
    r'^https?://(?:[a-z]+\.)?spotify\.(?:com|[a-z]{2,3})'
    r'(/((?:track|playlist|album|artist|show|episode)/)?)?'
)

CONTENT_TYPE_MAP = {
    'track': 'song',
    'playlist': 'playlist',
    'album': 'album',
    'artist': 'artist',
    'show': 'podcast show',
    'episode': 'podcast episode'
}



# regexes
spotify_regex = "^https?://(?:[a-z]+\.)?spotify\.(?:com|[a-z]{2,3})(/((?:track|playlist|album|artist|show|episode)/)?)?"