
from discord.ext.commands import DisabledCommand
class NotAllowedCommand(DisabledCommand):
    def __init__(self, message):
        self.message = message