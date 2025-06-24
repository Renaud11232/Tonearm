import inspect

from nextcord import voice_client, Client, abc


class TonearmVoiceClient(voice_client.VoiceClient):

    def __init__(self, client: Client, channel: abc.Connectable) -> None:
        self.__listeners = {}
        super().__init__(client, channel)

    def add_listener(self, event: str, listener):
        self.__get_listeners(event).append(listener)

    def __get_listeners(self, event: str):
        if event not in self.__listeners:
            self.__listeners[event] = []
        return self.__listeners[event]

    async def __exec_listeners(self, event: str, *params, **kwargs):
        for listener in self.__get_listeners(event):
            result = listener(*params, **kwargs)
            if inspect.isawaitable(result):
                await result

    async def disconnect(self, *, force: bool = False) -> None:
        await super().disconnect(force=force)
        await self.__exec_listeners("disconnect", force=force)