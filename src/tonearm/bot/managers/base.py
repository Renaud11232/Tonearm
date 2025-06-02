import logging
from abc import ABC, abstractmethod
import threading
from typing import TypeVar, Generic

KeyType = TypeVar('KeyType')
ServiceType = TypeVar('ServiceType')

class ManagerBase(ABC, Generic[KeyType, ServiceType]):

    def __init__(self):
        self.__lock = threading.Lock()
        self.__services = {}
        self.__logger = logging.getLogger("tonearm.managers")

    @abstractmethod
    def _create(self, key: KeyType) -> ServiceType:
        pass

    @abstractmethod
    def _get_id(self, key: KeyType) -> str | int:
        pass

    def get(self, key: KeyType) -> ServiceType:
        with self.__lock:
            id = self._get_id(key)
            if not id in self.__services:
                self.__services[id] = self._create(key)
                self.__logger.debug(f"Created new {type(self.__services[id]).__name__} for {type(key).__name__} {id}")
            return self.__services[id]

