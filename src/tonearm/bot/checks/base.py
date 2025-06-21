from abc import ABC, abstractmethod

import nextcord


class Check(ABC):

    @abstractmethod
    async def __call__(self, interaction: nextcord.Interaction) -> bool:
        raise Exception("Abstract method not implemented")