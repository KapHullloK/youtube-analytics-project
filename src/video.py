import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.environ.get('YT_API')


class Video:
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, id_video):
        try:
            self.id_video = id_video
            self._video = self.youtube.videos().list(part='snippet,statistics', id=self.id_video).execute()
            self.title = self._video['items'][0]['snippet']['title']
            self.url = self._video['items'][0]['snippet']['thumbnails']['default']['url']
            self.view_count = self._video['items'][0]['statistics']['viewCount']
            self.likes_count = self._video['items'][0]['statistics']['likeCount']
        except Exception:
            self.title = None
            self.url = None
            self.view_count = None
            self.likes_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, id_video, pl_id):
        super().__init__(id_video)
        self.plv_id = pl_id

    def __str__(self):
        return self.title
