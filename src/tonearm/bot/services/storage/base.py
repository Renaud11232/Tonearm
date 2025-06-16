import json
import pathlib
from abc import ABC


class StorageBase(ABC):

    def __init__(self, file_name):
        self.__file_name = file_name
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

    def set(self, key, value):
        parent = self.__data
        for k in key[:-1]:
            if k not in parent:
                parent[k] = {}
            parent = parent[k]
        parent[key[-1]] = value
        self.__save()

    def get(self, key, *, default=None):
        updated = False
        parent = self.__data
        for k in key[:-1]:
            if k not in parent:
                parent[k] = {}
                updated = True
            parent = parent[k]
        if key[-1] not in parent:
            parent[key[-1]] = default
            updated = True
        if updated:
            self.__save()
        return parent[key[-1]]
