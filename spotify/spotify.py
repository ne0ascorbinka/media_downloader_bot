from pyrogram import Client, filters
from pyrogram.types import Message
from concurrent.futures import ThreadPoolExecutor

import test_spotify
import credentials


app = Client("my_account",
             api_id=credentials.api_id,
             api_hash=credentials.api_hash)

# Create thread pools with separate queues for VIPs and other users
vip_pool_executor = ThreadPoolExecutor(max_workers=1)
other_pool_executor = ThreadPoolExecutor(max_workers=1)

@app.on_message(filters.regex("^https?://(?:[a-z]+\.)?spotify\.(?:com|[a-z]{2,3})(/((?:track|playlist|album|artist|show|episode)/)?)?"))
async def spotify_downloader(client: Client, message: Message):
    sent = await message.reply("Bitch, I am downloading")
    link = message.text

    if message.from_user.id in credentials.vip_ids:
        vip_pool_executor.submit(
            test_spotify.spotify_downloader,
            app,
            message.from_user.id,
            link,
            sent
        )
    else:
        other_pool_executor.submit(
            test_spotify.spotify_downloader,
            app,
            message.from_user.id,
            link,
            sent
        )


@app.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message):
   await message.reply("Bitch, I am alive")

# Define a filter to match incoming messages that contain audio files
audio_filter = filters.audio

# Define a handler function to respond to messages that match the filter
@app.on_message(audio_filter)
def handle_audio(client, message: Message):
    # Get the file ID of the audio file
    file_id = message.audio.file_id

    # Reply to the user with the file ID
    message.reply_text(f"The file ID of the song you sent is: {file_id}")
    app.send_cached_media(chat_id=message.from_user.id, file_id=file_id)

app.run()
