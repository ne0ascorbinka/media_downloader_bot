from pyrogram import Client
from config.config import config, chat_ids
from logs.logger import logger
from handlers.regular_handlers import RegularHandlers

class Bot:
    def __init__(self):
        self.client = self._initialize_client()
        self.greeter_client = self._initialize_client()
        self.load_chat_ids()
        self.set_handlers()

    def _initialize_client(self):
        return Client(config.BOT_NAME, api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

    def load_chat_ids(self):
        try:
            with open("chat_ids.txt", "r") as file:
                for line in file.readlines():
                    chat_ids.add(int(line))
        except FileNotFoundError:
            pass

    def set_handlers(self):
        RegularHandlers(self.client).register_handlers()

    async def notify_users(self):
        async with self.greeter_client:
            user = "neascorbinka"
            await self.greeter_client.send_message(user, "started!")

    def run(self):
        logger.debug("started!")
        self.greeter_client.run(self.notify_users())
        self.client.run() # Logic to run the bot

def main() -> None:
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()