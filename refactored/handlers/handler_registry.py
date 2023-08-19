from pyrogram import Client
from abc import ABC

class HandlerRegistry(ABC):
    def __init__(self, client: Client):
        self.client = client

    def register_handlers(self):
        raise NotImplementedError()