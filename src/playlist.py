import os
import datetime
import isodate

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.environ.get('YT_API')


class PlayList:
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self._playlist = self.youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
        self.title = self._playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self._playlist2 = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='snippet, contentDetails').execute()

        self.videos_id = [video['contentDetails']['videoId'] for video in self._playlist2['items']]
        self._videos_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                           id=','.join(self.videos_id)).execute()

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self._videos_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration

    def show_best_video(self):
        best_video = ''
        likes_max = 0
        for video in self._videos_response['items']:
            if int(video['statistics']['likeCount']) >= likes_max:
                best_video = video['id']
                likes_max = int(video['statistics']['likeCount'])
        return f"https://youtu.be/{best_video}"
