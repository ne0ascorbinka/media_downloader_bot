from pyrogram import Client
from pyrogram.types import (InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardButton, InlineKeyboardMarkup)
from pyrogram.handlers import InlineQueryHandler


# This is the example from pyrogram documentation. To you can allow inline
# mode for bots in botfather.
async def answer(client, inline_query: InlineQuery):
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Installation",
                input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/intro/install",
                description="How to install Pyrogram",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Open website",
                            url="https://docs.pyrogram.org/intro/install"
                        )]
                    ]
                )
            ),
            InlineQueryResultArticle(
                title="Usage",
                input_message_content=InputTextMessageContent(
                    "Here's how to use **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/start/invoking",
                description="How to use Pyrogram",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Open website",
                            url="https://docs.pyrogram.org/start/invoking"
                        )]
                    ]
                )
            )
        ],
        cache_time=1
    )

def set_inline_handlers(app: Client):
    app.add_handler(InlineQueryHandler(answer)) #in case if needed: filters.all