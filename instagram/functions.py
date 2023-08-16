# import re

# def is_valid_link(link):
#     """
#     Checks if a link is valid.

#     Args:
#         link (str): The link to check.

#     Returns:
#         bool: True if the link is valid, False otherwise.
#     """
#     regex = re.compile(
#         r'^(?:http|ftp)s?://'  # http:// or https:// or ftp:// or ftps://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain name
#         r'localhost|'  # localhost
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP address
#         r'(?::\d+)?'  # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#     return bool(re.match(regex, link))

# platforms = {"instagram": spotify_download(), "tiktok": tiktok_download(), "youtube": youtube_download(), "spotify": spotify_download()}

# def get_platform(link):
#     """
#     Returns the platform integer corresponding to the link.

#     Args:
#         link (str): The link to check.

#     Returns:
#         int: The platform integer corresponding to the link, or -1 if the link does not match any platform.
#     """
#     for platform, platform_int in platforms.items():
#         if platform in link:
#             return platform_int
#     return -1

def extract_url_code(instagram_post):
    """
    Extracts the URL code from an Instagram post link.

    Args:
        instagram_post (str): The Instagram post link.

    Returns:
        str: The URL code extracted from the link, or None if the link is invalid.
    """
    changing_url = instagram_post.split("/")
    url_code = changing_url[-2]
    return url_code


def spotify_download():
    # check what is this track/playlits/album
    ...

# do the same for youtube (shorts, video, music), instagram (reels, stories, videos, photos), tiktok

print(extract_url_code("https://www.instagram.com/volchanskaaa_/"))