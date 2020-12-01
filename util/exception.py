
from discord.ext.commands import DisabledCommand
class NotAllowedCommand(DisabledCommand):
    """Exception raised when a command is not allowed

    """
    def __init__(self, message):
        self.message = message