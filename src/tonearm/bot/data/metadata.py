class TrackMetadata:

    def __init__(self, url: str, title: str):
        self.__url = url
        self.__title = title

    @property
    def url(self):
        return self.__url

    @property
    def title(self):
        return self.__title