import json
import pathlib
import asyncio
from typing import List

from injector import noninjectable


class StorageService:

    @noninjectable("file_name")
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__lock = asyncio.Lock()
        try:
            with open(self.__file_name, 'r', encoding="utf-8") as f:
                self.__data = json.load(f)
        except FileNotFoundError:
            self.__data = {}
            self.__save()

    def __save(self):
        pathlib.Path(self.__file_name).parent.mkdir(parents=True, exist_ok=True)
        with open(self.__file_name, 'w', encoding="utf-8") as f:
            json.dump(self.__data, f, indent=2)

    async def set(self, key: str | List[str], value):
        key = self.__split_key(key)
        with self.__lock:
            parent = self.__data
            for k in key[:-1]:
                if k not in parent:
                    parent[k] = {}
                parent = parent[k]
            parent[key[-1]] = value
            self.__save()

    async def get(self, key: str | List[str], *, default=None):
        key = self.__split_key(key)
        with self.__lock:
            value = self.__data
            for k in key:
                if k not in value:
                    return default
                value = value[k]
            return value

    @staticmethod
    def __split_key(key: str | List[str]) -> List[str]:
        if isinstance(key, str):
            return key.split(".")
        return key