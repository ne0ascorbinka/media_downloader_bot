import json

class Config:
    def __init__(self, config_path="config.json"):
        with open(config_path) as file:
            data = json.load(file)
        
        self.BOT_NAME = data["bot_name"]
        self.API_ID = data["api_id"]
        self.API_HASH = data["api_hash"]
        self.BOT_USERNAME = data["bot_username"]
        self.BOT_TOKEN = data["bot_token"]
        self.ADMINS = data["allowed_users"]
        self.downloads_path = data["downloads_path"]
        self.logs_path = data["logs_path"]

config = Config()

chat_ids = set() # set of ids of bot users