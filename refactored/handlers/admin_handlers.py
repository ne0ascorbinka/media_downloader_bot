from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union
from utils import Analyzer
from handlers import HandlerRegistry
from logs.logger import logger
from config.config import config

class AdminHandlers(HandlerRegistry):
    def __init__(self, client: Client):
        super().__init__(client)
    
    def register_handlers(self):
        client = self.client

        client.add_handler(MessageHandler(AdminHandlers.show_admin_start, filters.command(["start", "back"]) & filters.user(config.ADMINS)))
        client.add_handler(CallbackQueryHandler(AdminHandlers.show_admin_start, filters.regex("admin_start")))

        client.add_handler(CallbackQueryHandler(AdminHandlers.stats_menu, filters.regex("stats")))
        client.add_handler(CallbackQueryHandler(AdminHandlers.select_period_menu, filters.regex("SP_.+"))) #stands for Select Period. ex.: SP_users
        client.add_handler(CallbackQueryHandler(AdminHandlers.select_type_menu, filters.regex("ST_.+"))) #stands for Select Type. ex.: ST_updates_day
        client.add_handler(CallbackQueryHandler(AdminHandlers.stats_results, filters.regex("SR_.+"))) #stands for Stats Results.


    
    @staticmethod
    async def show_admin_start(client: Client, update: Union[Message, CallbackQuery]):

        start_message = f"Welcome back to the bot! What would you like to do?"

        stats_button = InlineKeyboardButton("Get stats", callback_data="stats")
        user_mode_button = InlineKeyboardButton(
            "Switch to user mode", callback_data="user_start")

        markup = InlineKeyboardMarkup(
            [[stats_button, user_mode_button]])

        if isinstance(update, Message):
            await update.reply(start_message, reply_markup=markup)
        else:
            message = update.message
            await message.edit(start_message, reply_markup=markup)

    @staticmethod
    async def stats_menu(client: Client, callback_query: CallbackQuery):
        text = "Which stats would you like to know?"

        users_per_button = InlineKeyboardButton(
            "Users per period", callback_data="SP_users")
        queries_count_button = InlineKeyboardButton(
            "Updates count", callback_data="SP_updates")
        back_button = InlineKeyboardButton("Go back", callback_data="admin_start")
        markup = InlineKeyboardMarkup([[users_per_button, queries_count_button], [back_button]])

        await callback_query.message.edit(text, reply_markup=markup)
    
    @staticmethod
    async def select_period_menu(client: Client, callback_query: CallbackQuery):
        text = "Please, select a period"
        callback_data = callback_query.data[3:]

        daily_button = InlineKeyboardButton(
            "Today", callback_data=f"ST_{callback_data}_day")
        yesterday_button = InlineKeyboardButton(
            "Yesterday", callback_data=f"ST_{callback_data}_yesterday")
        week_button = InlineKeyboardButton(
            "Week", callback_data=f"ST_{callback_data}_week")
        month_button = InlineKeyboardButton(
            "Month", callback_data=f"ST_{callback_data}_month")
        markup = InlineKeyboardMarkup([[daily_button, yesterday_button], [
                                    week_button, month_button]])

        await callback_query.message.edit(text, reply_markup=markup)
    
    @staticmethod
    async def select_type_menu(client: Client, callback_query: CallbackQuery):
        text = "Please, select the type of query"
        callback_data = callback_query.data[3:]

        spotify_updates = InlineKeyboardButton(
            "Spotify", callback_data=f"SR_{callback_data}_spotify")
        youtube_updates = InlineKeyboardButton(
            "YouTube", callback_data=f"SR_{callback_data}_youtube")
        tiktok_updates = InlineKeyboardButton(
            "TikTok", callback_data=f"SR_{callback_data}_tiktok")
        markup = InlineKeyboardMarkup([[spotify_updates], [
                                    youtube_updates, tiktok_updates]])

        await callback_query.message.edit(text, reply_markup=markup)
    
    @staticmethod
    async def stats_results(client: Client, callback_query: CallbackQuery):
        data = callback_query.data[3:]
        stats_type = data.split('_')[0]
        period = data.split('_')[1]
        query_type = data.split('_')[2]


        descriptions = {
            "users": f"Active users for {period}: ",
            "updates": f"Updates of {query_type} type: "
        }

        analyzer = Analyzer.get_analyzer(stats_type, query_type)
        text = descriptions[stats_type] + str(analyzer.get_info_per_period(period))

        to_menu_button = InlineKeyboardButton("Back to menu", callback_data="admin_start")
        markup = InlineKeyboardMarkup([[to_menu_button]])

        await callback_query.message.edit(text, reply_markup=markup)