from googleapiclient.errors import HttpError

from src import channel


class Video(channel.Youtube):

    def __init__(self, video_id):
        """
        Инициализация атрибутов класса
        """

        # Получение информации о видео
        try:
            # Пробуем получить информацию о видео по переданному ID
            self.video_response = self.get_video_info(video_id)

            # Заполнение атрибутов соответствующими данными
            self.video_id = video_id
            self.video_title = self.video_response['items'][0]['snippet']['title']
            self.video_url = f'https://www.youtube.com/video/{self.video_id}'
            self.views_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
            self.duration = self.video_response['items'][0]['contentDetails']['duration']
        except (HttpError, IndexError):
            # В случае некорректного ID исключение HttpError не вызывается,
            # по ключу Items будет пустой список и при обращении к нему получим ошибку IndexError

            self.video_id = video_id
            self.title = None
            self.video_url = None
            self.views_count = None
            self.like_count = None
            self.duration = None

    def __str__(self):
        return self.video_title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """
        Инициализация атрибутов класса
        """

        super().__init__(video_id)
        self.playlist_id = playlist_id
