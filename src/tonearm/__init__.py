from injector import Injector

from tonearm.bot import Tonearm, BotModule
from tonearm.configuration import ConfigurationModule


def main():
    Injector([
        ConfigurationModule(),
        BotModule()
    ]).get(Tonearm).run()


if __name__ == "__main__":
    main()
