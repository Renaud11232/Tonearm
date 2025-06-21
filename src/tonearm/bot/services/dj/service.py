import nextcord

from injector import inject, noninjectable

from tonearm.bot.services.storage import StorageService

from .exceptions import DjException


class DjService:

    @inject
    @noninjectable("storage_service")
    def __init__(self, storage_service: StorageService):
        self.__storage_service = storage_service

    def add_role(self, role: nextcord.Role):
        roles = self.__storage_service.get_dj_roles()
        if role in roles:
            raise DjException(f"Members of {role.mention} are already DJs !")
        roles.append(role)
        self.__storage_service.set_dj_roles(roles)

    def remove_role(self, role: nextcord.Role):
        roles = self.__storage_service.get_dj_roles()
        try:
            roles.remove(role)
            self.__storage_service.set_dj_roles(roles)
        except ValueError:
            raise DjException(f"Members of {role.mention} aren't DJs !")

    def add(self, member: nextcord.Member):
        djs = self.__storage_service.get_dj_members()
        if member in djs:
            raise DjException(f"{member.mention} is already a DJ !")
        djs.append(member)
        self.__storage_service.set_dj_members(djs)

    def remove(self, member: nextcord.Member):
        djs = self.__storage_service.get_dj_members()
        try:
            djs.remove(member)
            self.__storage_service.set_dj_members(djs)
        except ValueError:
            raise DjException(f"{member.mention} isn't a DJ !")