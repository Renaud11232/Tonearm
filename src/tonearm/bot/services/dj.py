import discord

from injector import inject, noninjectable

from tonearm.bot.services.storage import StorageService
from tonearm.bot.exceptions import TranslatableException


class DjService:

    @inject
    @noninjectable("storage_service")
    def __init__(self, storage_service: StorageService):
        self.__storage_service = storage_service

    def add_role(self, role: discord.Role):
        roles = self.__storage_service.get_dj_roles()
        if role in roles:
            raise TranslatableException(
                "Members of {role} are already DJs !",
                role=role.mention
            )
        roles.append(role)
        self.__storage_service.set_dj_roles(roles)

    def remove_role(self, role: discord.Role):
        roles = self.__storage_service.get_dj_roles()
        try:
            roles.remove(role)
            self.__storage_service.set_dj_roles(roles)
        except ValueError:
            raise TranslatableException(
                "Members of {role} aren't DJs !",
                role=role.mention
            )

    def add_member(self, member: discord.Member):
        djs = self.__storage_service.get_dj_members()
        if member in djs:
            raise TranslatableException(
                "{member} is already a DJ !",
                member=member.mention
            )
        djs.append(member)
        self.__storage_service.set_dj_members(djs)

    def remove_member(self, member: discord.Member):
        djs = self.__storage_service.get_dj_members()
        try:
            djs.remove(member)
            self.__storage_service.set_dj_members(djs)
        except ValueError:
            raise TranslatableException(
                "{member} isn't a DJ !",
                member=member.mention
            )

    def add(self, member_or_role: discord.Member | discord.Role):
        if isinstance(member_or_role, discord.Member):
            self.add_member(member_or_role)
        else:
            self.add_role(member_or_role)

    def remove(self, member_or_role: discord.Member | discord.Role):
        if isinstance(member_or_role, discord.Member):
            self.remove_member(member_or_role)
        else:
            self.remove_role(member_or_role)