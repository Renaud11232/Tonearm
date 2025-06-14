from injector import singleton

from .base import MediaServiceBase


@singleton
class DirectUrlMediaService(MediaServiceBase):

    def __init__(self):
        super().__init__()

    def fetch(self, url: str) -> str:
        return url