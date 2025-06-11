from injector import Module, singleton, provider

from tonearm.cli import ArgumentParser, Configuration


class ConfigurationModule(Module):

    @singleton
    @provider
    def provide_configuration(self) -> Configuration:
        return ArgumentParser().parse_config()