import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv('YT_API')


class Channel:
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=API_KEY)

    def _print_json(self, data: dict) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self._print_json(channel)
