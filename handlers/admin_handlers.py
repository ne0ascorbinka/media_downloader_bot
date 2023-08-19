from typing import Union
from functions import dynamic_data_filter, Analyzer
from pyrogram import Client, filters
from pyrogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from credentials import ADMINS, BOT_NAME, chat_ids

async def show_admin_start(client: Client, update: Union[Message, CallbackQuery]):

    start_message = f"Welcome back to the {BOT_NAME}! What would you like to do?"

    stats_button = InlineKeyboardButton("Get stats", callback_data="stats")
    post_button = InlineKeyboardButton("Post", callback_data="post")
    user_mode_button = InlineKeyboardButton(
        "Switch to user mode", callback_data="user_start")

    markup = InlineKeyboardMarkup(
        [[stats_button, post_button], [user_mode_button]])

    if isinstance(update, Message):
        await update.reply(start_message, reply_markup=markup)
    else:
        message = update.message
        await message.edit(start_message, reply_markup=markup)

async def show_stats_menu(client: Client, callback_query: CallbackQuery):
    text = "Which stats would you like to know?"

    users_per_button = InlineKeyboardButton(
        "Users per period", callback_data="users")
    queries_count_button = InlineKeyboardButton(
        "Updates count", callback_data="updates")
    success_count_button = InlineKeyboardButton(
        "Successes count", callback_data="successes")
    back_button = InlineKeyboardButton("Go back", callback_data="admin_start")
    markup = InlineKeyboardMarkup([[users_per_button, queries_count_button], [
                                  success_count_button, back_button]])

    await callback_query.message.edit(text, reply_markup=markup)

async def select_period_menu(client: Client, callback_query: CallbackQuery):
    text = "Please, select a period"

    daily_button = InlineKeyboardButton(
        "Today", callback_data=f"{callback_query.data}_day")
    yesterday_button = InlineKeyboardButton(
        "Yesterday", callback_data=f"{callback_query.data}_yesterday")
    week_button = InlineKeyboardButton(
        "Week", callback_data=f"{callback_query.data}_week")
    month_button = InlineKeyboardButton(
        "Month", callback_data=f"{callback_query.data}_month")
    back_button = InlineKeyboardButton("Go back", callback_data="stats")
    markup = InlineKeyboardMarkup([[daily_button, yesterday_button], [
                                  week_button, month_button], [back_button]])

    await callback_query.message.edit(text, reply_markup=markup)

async def select_type_menu(client: Client, callback_query: CallbackQuery):
    text = "Please, select the type of query"

    spotify_updates = InlineKeyboardButton(
        "Spotify", callback_data=f"{callback_query.data}_spotify")
    instagram_updates = InlineKeyboardButton(
        "Instagram", callback_data=f"{callback_query.data}_instagram")
    youtube_updates = InlineKeyboardButton(
        "YouTube", callback_data=f"{callback_query.data}_youtube")
    tiktok_updates = InlineKeyboardButton(
        "TikTok", callback_data=f"{callback_query.data}_tiktok")
    back = InlineKeyboardButton("Go back", callback_data='_'.join(
        callback_query.data.split('_')[:-1]))
    markup = InlineKeyboardMarkup([[spotify_updates, instagram_updates], [
                                  youtube_updates, tiktok_updates], [back]])

    await callback_query.message.edit(text, reply_markup=markup)

async def stats_results(client: Client, callback_query: CallbackQuery):
    stats_type = callback_query.data.split('_')[0]
    period = callback_query.data.split('_')[1]
    query_type = callback_query.data.split('_')[-1]
    descriptions = {
        "users": f"Active users for {period}: ",
        "updates": f"Updates of {query_type} type: ",
        "successes": f"Successes statistics of {query_type} type: "
    }

    analyzer = Analyzer.get_analyzer(stats_type, query_type)
    text = descriptions[stats_type] + str(analyzer.get_info_per_period(period))

    back_button = InlineKeyboardButton(
        "Go back", callback_data='_'.join(
            callback_query.data.split('_')[
                :-1]))  # I could implement literally back button but I don't give a shit
    markup = InlineKeyboardMarkup([[back_button]])

    await callback_query.message.edit(text, reply_markup=markup)

async def post(client: Client, message: Message):
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    text = f"<a href=\"{link}\">Greetings</a> from **Pyrogram**!"
    button = InlineKeyboardButton("Open some link", url=link)
    markup = InlineKeyboardMarkup([[button]])

    for id in chat_ids:
        await client.send_message(id, text=text, reply_markup=markup, disable_web_page_preview=True)

def set_admin_handlers(app: Client):
    app.add_handler(MessageHandler(show_admin_start, filters.command("start") & filters.user(ADMINS)))
    app.add_handler(CallbackQueryHandler(show_admin_start, dynamic_data_filter("admin_start")
                       & filters.user(ADMINS)))
    
    app.add_handler(CallbackQueryHandler(show_stats_menu, dynamic_data_filter("stats")))
    
    app.add_handler(CallbackQueryHandler(select_period_menu, dynamic_data_filter(["users", "updates", "successes"])))

    # its not effective since to check the correspondance filter searches throughout the whole list which is O(N)
    # while if we write our own filter which deconstructs callback_query's
    # data it will take time O(1) but I fucked its mouths 
    # better use regexes
    typed_stats_types = ("updates", "successes")
    periods = ("day", "yesterday", "week", "month")

    datas = []
    for type in typed_stats_types:
        for period in periods:
            datas.append("_".join((type, period)))
    
    app.add_handler(CallbackQueryHandler(select_type_menu, dynamic_data_filter(datas)))

    queries = ("tiktok", "spotify", "instagram", "youtube")
    datas = [f"{data}_{query}" for data in datas for query in queries]
    datas += [f"users_{period}" for period in periods]
    
    app.add_handler(CallbackQueryHandler(stats_results, dynamic_data_filter(datas)))

    app.add_handler(MessageHandler(post, filters.user(ADMINS) & filters.command("post")))
    app.add_handler(CallbackQueryHandler(post, filters.user(ADMINS) & dynamic_data_filter("post")))