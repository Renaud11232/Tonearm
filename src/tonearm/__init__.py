from injector import Injector

from tonearm.bot import Tonearm
from tonearm.cli.action import EnvDefault
from tonearm.modules import ConfigurationModule, BotModule


def main():
    Injector([
        ConfigurationModule(),
        BotModule()
    ]).get(Tonearm).run()


if __name__ == "__main__":
    main()
