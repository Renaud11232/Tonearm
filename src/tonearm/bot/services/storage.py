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

    async def __set(self, key: str | List[str], value):
        key = self.__split_key(key)
        async with self.__lock:
            parent = self.__data
            for k in key[:-1]:
                if k not in parent:
                    parent[k] = {}
                parent = parent[k]
            parent[key[-1]] = value
            self.__save()

    async def __get(self, key: str | List[str], *, default=None) -> Any:
        key = self.__split_key(key)
        async with self.__lock:
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
        return await self.__get("volume", default=100)

    async def set_volume(self, volume: int):
        await self.__set("volume", volume)

    async def get_dj_roles(self) -> List[nextcord.Role]:
        roles = await self.__get("dj.roles", default=[])
        return [self.__guild.get_role(role) for role in roles]

    async def set_dj_roles(self, dj_roles: List[nextcord.Role]):
        roles = [role.id for role in dj_roles]
        return await self.__set("dj.roles", roles)

    async def get_dj_members(self) -> List[nextcord.Member]:
        members = await self.__get("dj.members", default=[])
        return [self.__guild.get_member(member) for member in members]

    async def set_dj_members(self, dj_members: List[nextcord.Member]):
        members = [member.id for member in dj_members]
        return await self.__set("dj.members", members)

    async def set_channel(self, channel: nextcord.TextChannel | None):
        await self.__set("channel", None if channel is None else channel.id)

    async def get_channel(self) -> nextcord.TextChannel | None:
        channel = await self.__get("channel", default=None)
        return None if channel is None else self.__guild.get_channel(channel)

    async def set_anarchy(self, anarchy: bool):
        await self.__set("anarchy", anarchy)

    async def get_anarchy(self) -> bool:
        return await self.__get("anarchy", default=False)