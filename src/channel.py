import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv('YT_API')


class Channel:
    def __init__(self, channel_id: str) -> None:
        self.__channel_id = channel_id

        self._youtube = build('youtube', 'v3', developerKey=API_KEY)
        self._channel = self._youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self._channel["items"][0]["snippet"]["title"]
        self.description = self._channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/" + self._channel["items"][0]["snippet"]["customUrl"]
        self.subscribers = self._channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self._channel["items"][0]["statistics"]["videoCount"]
        self.views = self._channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)

    def to_json(self, file):
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(directory, file)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.append({
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "views": self.views,
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False)
