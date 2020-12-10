from util.exception import NotAllowedCommand
from game.match import Match
from util.strings import get_string_bot as _


# This class store the matches for each server
class StarterHelper:
    """A class to store the matches for each server and channel. It helps also to change the status.

           """
    def __init__(self):
        self.matches = dict()

    def start(self, guild, channel):
        if (guild.id, channel.id) not in self.matches.keys():
            self.matches[(guild.id, channel.id)] = Match(guild, channel)
        self.matches[(guild.id, channel.id)].start()

    def join(self, guild_id, channel_id, member):
        if (guild_id, channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].join(member)
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def leave(self, guild_id, channel_id, member):
        if (guild_id, channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].leave(member)
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def play(self, guild_id, channel_id, tag):
        if (guild_id, channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].play(tag)
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def stop(self, guild_id, channel_id):
        if (guild_id, channel_id) in self.matches.keys():
            self.matches[(guild_id, channel_id)].stop()
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def print_status(self):
        """print the status

            """
        s = 'Match'
        for m in self.matches.keys():
            s += self.matches[m].print_status()
        return s
