from nextcord.ext import commands


class CommandCogBase(commands.Cog):

    def __init__(self):
        super().__init__()

    def _add_checks(self, *commands, checks):
        for command in commands:
            for check in checks:
                command.checks.append(check.predicate)