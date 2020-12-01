from enum import Enum

from game.colorgame import ColorGame
from game.team import Team
from game.word import WordTable
from util.exception import NotAllowedCommand

class Status(Enum):
    """A class to represent the possible status for a match

       """
    NOT_STARTED = 1 #: it is a not joinable match just instantiated
    JOINABLE = 2 #: it is a match in which players can join in.
    PLAY = 3 #: it is a match started and players can't join in
    STOPPED = 4 #: it is a match stopped

class Match():
    """A class to represent the match. It stores the guild, the channel, the list of members, the status and if the status of
    the match is Status.PLAY also the StartedMatch object.

       """
    def __init__(self, guild, channel):
        self.guild = guild
        self.channel = channel
        self.members = dict()
        self.status = Status.NOT_STARTED
        self.team_red = Team(ColorGame.RED, 'Red')
        self.team_blue = Team(ColorGame.BLUE, 'Blue')

    def join(self, member):
        if self.status == Status.JOINABLE:
            self.members[member.id] = member
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is started')
        else:
            raise NotAllowedCommand('The match is not started')

    def leave(self, member):
        if self.status == Status.JOINABLE:
            if member.id in self.members.keys():
                self.members.pop(member.id)
            else:
                raise NotAllowedCommand('You are not in the playing list')
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is started')
        else:
            raise NotAllowedCommand('The match is not started')

    def start(self):
        if self.status == Status.JOINABLE:
            raise NotAllowedCommand('The match is already started')
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is already started and in progress')
        else:
            self.members = dict()
            self.status = Status.JOINABLE

    def play(self, tag):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand('The match is not started')
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is already started and in progress')
        else:
            self.status = Status.PLAY
            self.grid_table = WordTable()
            self.grid_table.generate_words(tag)

    def stop(self):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand('The match is already not started')
        else:
            self.status = Status.STOPPED
            self.started_match = None

    def print_status(self):
        s = "Guild id: {}, channel id: {}, status: {} \nMembers:\n".format(self.guild.name, self.channel.name, self.status)
        for m in self.members.keys():
            s += self.members[m].name + '\n'
        s += self.team_red.print_status() + '\n' + self.team_blue.print_status() + '\n'
        if self.status == Status.PLAY:
            s += self.grid_table.print_status()
        if s == '':
            return 'no match found'
        return s

    def join_as_captain(self, member):
        """Joins the member to one team if available

           Args:
               member: A member instance

           Returns:
               A string with the name of the team

           Raises:
               NotAllowedCommand: An error occured when there are not spaces to be master available
           """
        if self.status != Status.JOINABLE:
            raise NotAllowedCommand('The match is not joinable')
        else:
            if member.id in self.members.keys():
                return self.join_team(member)
            else:
                raise NotAllowedCommand('You have to join at the match')

    def join_team(self, member):
        if self.team_red.master == None:
            self.team_red.set_master(member)
            return self.team_red.name
        elif self.team_blue.master == None:
            self.team_blue.set_master(member)
            return self.team_blue.name
        else:
            raise NotAllowedCommand('Master is already set')
