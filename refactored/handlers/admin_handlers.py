from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union
from handlers import HandlerRegistry
from logs.logger import logger
from config.config import config

class AdminHandlers(HandlerRegistry):
    def __init__(self, client: Client):
        super().__init__(client)
    
    def register_handlers(self):
        client = self.client

        client.add_handler(MessageHandler(AdminHandlers.show_admin_start, filters.command("start") & filters.user(config.ADMINS)))
        client.add_handler(CallbackQueryHandler(AdminHandlers.show_admin_start, filters.regex("admin_start")))

        client.add_handler(CallbackQueryHandler(AdminHandlers.stats, filters.regex("stats")))
    
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
    async def stats(client: Client, callback_query: CallbackQuery):
        back_button = InlineKeyboardButton("Go back", callback_data="admin_start")
        markup = InlineKeyboardMarkup([[back_button]])
        await callback_query.message.edit("No stats yet :(", reply_markup=markup)
    # TODO: make stats