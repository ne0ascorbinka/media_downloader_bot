"""
Spotify module with all necessary functions.
Don't wonder why it's called test_spotify
"""

from credentials import *
# from credentials import *
import os
import platform
from logger import logger, Status

from pyrogram import Client
from pyrogram.types import Message

dictionary_of_links = dict()

# TODO: ADD PATH WAY TO FCKING SPOT-DL COMMAND so we don't have to jump between fucking dirs

def change_to_root_folder():
    os.chdir(ROOT_FOLDER_PATH)


# check if there is a file_id in dict
def check_file_id_in_dict(app, user_id, link):
    if link in dictionary_of_links:
        file_id = dictionary_of_links[link]
        the_type_of_set = set()
        if type(file_id) == type(the_type_of_set):
            for i in file_id:
                app.send_audio(chat_id=user_id, audio=i)
        else:
            app.send_audio(chat_id=user_id, audio=file_id)
        return True
    else:
        return False


# create a folder for a user if there are no file_id
def create_user_folder(user_id):
    folder_for_current_user = os.path.join(ROOT_FOLDER_PATH, str(user_id))
    os.makedirs(folder_for_current_user, exist_ok=True)
    os.chdir(folder_for_current_user)
    return folder_for_current_user


# download songs\a song
def download_spotify_files(link):
    os.system(f'spotdl "{link}"')


# send to a user and add to a dictionary
def send_to_a_user(app, user_id, folder_for_current_user, link):
    if len(os.listdir(folder_for_current_user)) > 1:
        set_of_file_ids = set()
        for filename in os.listdir(folder_for_current_user):
            full_path = os.path.join(folder_for_current_user, filename)
            sent_file = app.send_document(chat_id=user_id, document=full_path)
            file_id = sent_file.audio.file_id
            set_of_file_ids.add(file_id)  # Updated this line
        dictionary_of_links[link] = set_of_file_ids
        return set_of_file_ids
    else:
        for filename in os.listdir(folder_for_current_user):
            full_path = os.path.join(folder_for_current_user, filename)
            sent_file = app.send_document(chat_id=user_id, document=full_path)
            file_id = sent_file.audio.file_id
            dictionary_of_links[link] = file_id  # Updated this line
        return file_id



# remove from the folder
def remove_user_folder(folder_for_current_user):
    change_to_root_folder()
    if platform.system() == "Windows":
        os.system(f'rmdir /s /q "{folder_for_current_user}"')
    else:
        os.system(f'rm -r "{folder_for_current_user}"')



def add_to_dictionary_file_id_and_a_link(link, file_id):
    dictionary_of_links[link] = file_id


def spotify_downloader(app: Client, user_id: int, link: str, sent: Message):
    try: 
        if check_file_id_in_dict(app=app, user_id=user_id, link=link):
            sent.delete()
            return
        folder_for_current_user = create_user_folder(user_id)
        download_spotify_files(link)
        file_id = send_to_a_user(app, user_id, folder_for_current_user, link)
        sent.delete()
        if file_id is not None:
            add_to_dictionary_file_id_and_a_link(link=link, file_id=file_id)
        remove_user_folder(folder_for_current_user)
        logger.info(
            f"handling spotify link",
            extra={
                "id": sent.chat.id,
                "status": Status.SUCCESS})
    except Exception as e:
        logger.error(str(e), extra={
            "id" : id,
            "status" : Status.FAILURE
        })
        logger.warn(f"Following message content caused an exception above: {link}", extra={
            "id" : id,
            "status" : Status.FAILURE})
