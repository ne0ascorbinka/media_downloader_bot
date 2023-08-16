from credentials import *
import os
import platform
import threading
from pathlib import Path

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

dictionary_of_links = dict()
lock = threading.Lock()

# Spotify authentication
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET))

def change_to_root_folder():
    os.chdir(ROOT_FOLDER_PATH)

def check_file_id_in_dict(app, user_id, link):
    with lock:
        if link in dictionary_of_links:
            file_id = dictionary_of_links[link]
            app.send_audio(chat_id=user_id, audio=file_id)
            return True
        else:
            return False

def create_user_folder(user_id):
    folder_for_current_user = Path(ROOT_FOLDER_PATH, str(user_id))
    folder_for_current_user.mkdir(parents=True, exist_ok=True)
    return folder_for_current_user

def download_spotify_files(link):
    # Replace this with the code to download the Spotify files using spotipy

def send_to_a_user(app, user_id, folder_for_current_user, link):
    # ...

def remove_user_folder(folder_for_current_user):
    # ...

def add_to_dictionary_file_id_and_a_link(link, file_id):
    with lock:
        dictionary_of_links[link] = file_id

def spotify_downloader(app, user_id, link, sent):
    # ...
