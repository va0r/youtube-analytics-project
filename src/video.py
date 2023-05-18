from src.channel import Channel


class Video:
    """
    Инициализация класса
    """

    def __init__(self, video_id):
        self.__video_id = video_id
        self.__video = self.video
        self.__title = self.title
        self.__url = self.url
        self.__view_count = self.view_count
        self.__likes_count = self.likes_count

    @property
    def video_id(self):
        """
        Возвращает id видео
        """
        return self.__video_id

    @property
    def video(self):
        """
        Запрос к youtube по определенному id
        """
        return Channel.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.__video_id
        ).execute()

    @property
    def title(self):
        """
        Возвращает данные видео
        """
        return self.video['items'][0]['snippet']['title']

    @property
    def url(self):
        """
        Возвращает ссылку на видео
        """
        return f'https://www.youtube.com/watch?v={self.__video_id}'

    @property
    def view_count(self):
        """
        Возвращает количество просмотров
        """
        return self.video['items'][0]['statistics']['viewCount']

    @property
    def likes_count(self):
        """
        Возвращает количество лайков
        """
        return self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Класс для видео `PLVideo`, который инициализирует 'id видео' и 'id плейлиста из класса Video'
    """

    def __init__(self, video_id, playlist_id):
        self.__video_id = video_id
        self.__playlist_id = playlist_id
        super().__init__(video_id)
