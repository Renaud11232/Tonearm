import json
import pathlib
import asyncio
from typing import List, Any

import nextcord

from injector import noninjectable, inject


class StorageService:

    @noninjectable("file_name")
    @inject
    def __init__(self, guild: nextcord.Guild, file_name: str):
        self.__guild = guild
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

    def __set(self, key: str | List[str], value):
        key = self.__split_key(key)
        parent = self.__data
        for k in key[:-1]:
            if k not in parent:
                parent[k] = {}
            parent = parent[k]
        parent[key[-1]] = value
        self.__save()

    def __get(self, key: str | List[str], *, default=None) -> Any:
        key = self.__split_key(key)
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

    async def get_volume(self) -> int:
        async with self.__lock:
            return self.__get("volume", default=100)

    async def set_volume(self, volume: int):
        async with self.__lock:
            self.__set("volume", volume)

    async def get_dj_roles(self) -> List[nextcord.Role]:
        async with self.__lock:
            int_roles = self.__get("dj.roles", default=[])
            roles = list(filter(lambda role: role is not None, map(self.__guild.get_role, int_roles)))
            if len(int_roles) > len(roles):
                self.__set_dj_roles(roles)
            return roles

    def __set_dj_roles(self, roles: List[nextcord.Role]):
            int_roles = list(map(lambda role: role.id, roles))
            self.__set("dj.roles", int_roles)

    async def set_dj_roles(self, dj_roles: List[nextcord.Role]):
        async with self.__lock:
            self.__set_dj_roles(dj_roles)

    async def get_dj_members(self) -> List[nextcord.Member]:
        async with self.__lock:
            int_members = self.__get("dj.members", default=[])
            members = list(filter(lambda member: member is not None, map(self.__guild.get_member, int_members)))
            if len(int_members) > len(members):
                self.__set_dj_members(members)
            return members

    def __set_dj_members(self, members: List[nextcord.Member]):
        int_members = list(map(lambda member: member.id, members))
        self.__set("dj.members", int_members)

    async def set_dj_members(self, members: List[nextcord.Member]):
        async with self.__lock:
            self.__set_dj_members(members)

    async def get_channel(self) -> nextcord.TextChannel | None:
        async with self.__lock:
            int_channel = self.__get("channel", default=None)
            channel = self.__guild.get_channel(int_channel)
            if int_channel is not None and channel is None:
                self.__set_channel(None)
            return channel

    def __set_channel(self, channel: nextcord.TextChannel | None):
        int_channel = channel.id if channel is not None else None
        self.__set("channel", int_channel)

    async def set_channel(self, channel: nextcord.TextChannel | None):
        async with self.__lock:
            self.__set_channel(channel)

    async def get_anarchy(self) -> bool:
        async with self.__lock:
            return self.__get("anarchy", default=False)

    async def set_anarchy(self, anarchy: bool):
        async with self.__lock:
            self.__set("anarchy", anarchy)