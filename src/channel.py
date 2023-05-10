import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

from env_sett import ENV_FILE

load_dotenv(ENV_FILE)


class Channel:
    """
    Класс для ютуб-канала.
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        return cls.youtube

    def to_json(self, filename: str):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel.
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.__dict__, file, ensure_ascii=False, indent=4)

    def __str__(self):
        return f"{self.title}, ({self.url})"

    def __add__(self, redactsiya) -> int:
        if isinstance(redactsiya, Channel):
            return self.subscriber_count + redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __sub__(self, redactsiya) -> int:
        if isinstance(redactsiya, Channel):
            return self.subscriber_count - redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __gt__(self, redactsiya):  # >
        if isinstance(redactsiya, Channel):
            return self.subscriber_count > redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __ge__(self, redactsiya) -> int:  # >=
        if isinstance(redactsiya, Channel):
            return self.subscriber_count >= redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __lt__(self, redactsiya):  # <
        if isinstance(redactsiya, Channel):
            return self.subscriber_count < redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __le__(self, redactsiya):  # <=
        if isinstance(redactsiya, Channel):
            return self.subscriber_count <= redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __eq__(self, redactsiya):  # ==
        if isinstance(redactsiya, Channel):
            return self.subscriber_count == redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")
