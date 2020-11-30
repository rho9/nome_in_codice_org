from enum import Enum

from game.colorgame import ColorGame
from game.team import Team
from util.exception import NotAllowedCommand

class Status(Enum):
    NOT_STARTED = 1
    JOINABLE = 2
    PLAY = 3
    STOPPED = 4

class Match():
    def __init__(self, guild, channel):
        self.guild = guild
        self.channel = channel
        self.members = dict()
        self.status = Status.NOT_STARTED
        self.started_match = None

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

    def play(self):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand('The match is not started')
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is already started and in progress')
        else:
            self.status = Status.PLAY
            self.started_match = StartedMatch(self)

    def stop(self):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand('The match is already not started')
        else:
            self.status = Status.STOPPED
            self.started_match = None

    def print_status(self):
        s = "Guild id: {}, channel id: {}, status: {} \nMembers:\n".format(self.guild.name, self.channel.name, self.status)
        for m in self.members.keys():
            s+= self.members[m].name + '\n'
        if self.status == Status.PLAY:
            s += self.started_match.print_status()
        if s == '':
            return 'no match found'
        return s

    def join_as_captain(self, member):
        if self.status != Status.PLAY:
            raise NotAllowedCommand('The match is not already started')
        else:
            if member.id in self.members.keys():
                return self.started_match.join_as_captain(member)
            else:
                raise NotAllowedCommand('Not joined')


class StartedMatch():
    def __init__(self, match):
        self.match = match
        self.team_red = Team(ColorGame.RED, 'Red')
        self.team_blue = Team(ColorGame.BLUE, 'Blue')

    def join_as_captain(self, member):
        if self.team_red.master == None:
            self.team_red.set_master(member)
            return 'red'
        elif self.team_blue.master == None:
            self.team_blue.set_master(member)
            return 'blue'
        else:
            raise NotAllowedCommand('Master is already set')

    def print_status(self):
        return self.team_red.print_status() + '\n' + self.team_blue.print_status()