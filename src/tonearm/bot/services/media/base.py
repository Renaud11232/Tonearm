from abc import ABC, abstractmethod


class MediaServiceBase(ABC):

    @abstractmethod
    async def fetch(self, url: str) -> str:
        pass