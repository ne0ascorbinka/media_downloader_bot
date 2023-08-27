from abc import ABC
from pyrogram import Client
import os
import shutil
import traceback
from logs import logger

class BaseDownloader(ABC):
    def __init__(self, client: Client, id: int, url: str) -> None:
        self.client = client
        self.id = id
        self.url = url
        self.folder_path = str(self.id)
        self.sent_message = None
        self.callback_query = None
        self.query_type = None
    
    def start(self) -> None:
        self._create_folder()

        try:
            self.download()
            self._upload()
            logger.info("successfully handled link", extra={"id" : self.id, "query" : self.query_type})
        except Exception as exception:
            if self.sent_message:
                self.sent_message.edit("Error occured :(")
            elif self.callback_query:
                self.callback_query.message.edit("Error occured :(")
            traceback.print_exc()
            logger.warning(f"this url coused an error: {self.url}", extra={"id" : self.id, "query" : self.query_type})
            logger.error(f"error occured: {str(exception)}", extra={"id" : self.id, "query" : self.query_type})

        
        self._delete_media()
    
    def _create_folder(self) -> None:
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def download(self) -> None:
        raise NotImplementedError()
    
    def _upload(self) -> None:
        raise NotImplementedError()
    
    def _delete_media(self) -> None:
        if os.path.exists(self.folder_path):
            shutil.rmtree(self.folder_path)
