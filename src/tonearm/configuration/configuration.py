class Configuration:

    def __init__(self,
                 discord_token: str,
                 log_level: str,
                 youtube_api_key: str,
                 cobalt_api_url: str,
                 cobalt_api_key: str | None,
                 data_path: str,
                 buffer_length: int):
        self.__discord_token = discord_token
        self.__log_level = log_level
        self.__youtube_api_key = youtube_api_key
        self.__cobalt_api_url = cobalt_api_url
        self.__cobalt_api_key = cobalt_api_key
        self.__data_path = data_path
        self.__buffer_length = buffer_length

    @property
    def discord_token(self) -> str:
        return self.__discord_token

    @property
    def log_level(self) -> str:
        return self.__log_level

    @property
    def youtube_api_key(self) -> str:
        return self.__youtube_api_key

    @property
    def cobalt_api_url(self) -> str:
        return self.__cobalt_api_url

    @property
    def cobalt_api_key(self) -> str:
        return self.__cobalt_api_key

    @property
    def data_path(self) -> str:
        return self.__data_path

    @property
    def buffer_length(self) -> int:
        return self.__buffer_length
    