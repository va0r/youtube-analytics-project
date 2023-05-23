import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

from env_sett import ENV_FILE

load_dotenv(ENV_FILE)


class Youtube:
    """Базовый класс для работы с видео, плейлистами и каналами"""

    __API_KEY: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__API_KEY)

    @classmethod
    def get_playlist_info(cls, playlist_id: str) -> dict:
        """
        Метод для получения информации о плейлисте Youtube по его id
        """

        playlist_response = cls.__youtube.playlists().list(id=playlist_id,
                                                           part='contentDetails,snippet',
                                                           maxResults=50,
                                                           ).execute()
        return playlist_response

    @classmethod
    def get_video_info(cls, video_id: str) -> dict:
        """Метод для получения информации о видео из Youtube по его id"""

        video_response = cls.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
        return video_response

    @classmethod
    def get_channel_info(cls, channel_id: str) -> dict:
        """Метод для получения информации о канале Youtube по его id"""

        channel_response = cls.__youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        return channel_response

    @classmethod
    def get_videos_from_playlist(cls, playlist_id: str) -> dict:
        """Получение информации о всех видео из плейлиста"""
        playlist_videos = cls.__youtube.playlistItems().list(playlistId=playlist_id,
                                                             part='contentDetails',
                                                             maxResults=50,
                                                             ).execute()
        return playlist_videos

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API вне класса"""
        return cls.__youtube


class Channel(Youtube):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.get_channel_info(channel_id)
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscribers_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        """Свойство для обращения к приватному атрибуту __channel_id"""
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name: str) -> None:
        """Запись информации о канале в file_name.json"""
        with open(file_name, 'w') as json_file:
            json.dump(self.channel, json_file, ensure_ascii=False)

    def __str__(self) -> str:
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        """Сложение классов по количеству подписчиков"""
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other) -> int:
        """Разность классов по количеству подписчиков"""
        if isinstance(other, Channel):
            return int(self.subscribers_count) - int(other.subscribers_count)
        else:
            raise TypeError("ERROR")

    def __ge__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        if isinstance(other, Channel):
            return int(self.subscribers_count) >= int(other.subscribers_count)
        else:
            raise TypeError("ERROR")

    def __gt__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        if isinstance(other, Channel):
            return int(self.subscribers_count) > int(other.subscribers_count)
        else:
            raise TypeError("ERROR")

    def __lt__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        if isinstance(other, Channel):
            return int(self.subscribers_count) < int(other.subscribers_count)
        else:
            raise TypeError("ERROR")

    def __le__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        if isinstance(other, Channel):
            return int(self.subscribers_count) <= int(other.subscribers_count)
        else:
            raise TypeError("ERROR")

    def __eq__(self, other) -> bool:
        """Сравнение классов по количеству подписчиков"""
        if isinstance(other, Channel):
            return int(self.subscribers_count) == int(other.subscribers_count)
        else:
            raise TypeError("ERROR")
