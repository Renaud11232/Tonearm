from injector import Injector

from tonearm.app import Tonearm
from tonearm.bot import BotModule
from tonearm.configuration import ConfigurationModule

def main():
    Injector([
        ConfigurationModule(),
        BotModule()
    ]).get(Tonearm).run()


if __name__ == "__main__":
    main()
