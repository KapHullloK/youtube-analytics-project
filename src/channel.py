import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv('YT_API')


class Channel:
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id

        self.__youtube = build('youtube', 'v3', developerKey=API_KEY)
        self.__channel = self.__youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = self.__channel["items"][0]["snippet"]["title"]
        self.description = self.__channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/" + self.__channel["items"][0]["snippet"]["customUrl"]
        self.subscribers = self.__channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.__channel["items"][0]["statistics"]["videoCount"]
        self.views = self.__channel["items"][0]["statistics"]["viewCount"]

    @property
    def info_channel(self):
        return self.__channel

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
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "views": self.views,
        })

        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False)
