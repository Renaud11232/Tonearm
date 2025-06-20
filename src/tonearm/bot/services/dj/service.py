import asyncio

import nextcord

from injector import inject, noninjectable

from tonearm.bot.services.storage import StorageService

from .exceptions import DjException


class DjService:

    @inject
    @noninjectable("storage_service")
    def __init__(self, storage_service: StorageService):
        self.__storage_service = storage_service
        self.__lock = asyncio.Lock()

    async def add_role(self, role: nextcord.Role):
        async with self.__lock:
            roles = await self.__storage_service.get_dj_roles()
            if role in roles:
                raise DjException(f"Members of {role.mention} are already DJs !")
            roles.append(role)
            await self.__storage_service.set_dj_roles(roles)

    async def remove_role(self, role: nextcord.Role):
        async with self.__lock:
            roles = await self.__storage_service.get_dj_roles()
            try:
                roles.remove(role)
                await self.__storage_service.set_dj_roles(roles)
            except ValueError:
                raise DjException(f"Members of {role.mention} aren't DJs !")

    async def add(self, member: nextcord.Member):
        async with self.__lock:
            djs = await self.__storage_service.get_dj_members()
            if member in djs:
                raise DjException(f"{member.mention} is already a DJ !")
            djs.append(member)
            await self.__storage_service.set_dj_members(djs)

    async def remove(self, member: nextcord.Member):
        async with self.__lock:
            djs = await self.__storage_service.get_dj_members()
            try:
                djs.remove(member)
                await self.__storage_service.set_dj_members(djs)
            except ValueError:
                raise DjException(f"{member.mention} isn't a DJ !")