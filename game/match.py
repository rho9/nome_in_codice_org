from enum import Enum
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

    def join(self, memb):
        if self.status == Status.JOINABLE:
            self.members[memb.id] = memb
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is started')
        else:
            raise NotAllowedCommand('The match is not started')

    def leave(self, memb):
        if self.status == Status.JOINABLE:
            if memb.id in self.members.keys():
                self.members.pop(memb.id)
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

    def stop(self):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand('The match is already not started')
        else:
            self.status = Status.STOPPED

    def print_status(self):
        s = "Guild id: {}, channel id: {}, status: {} \nMembers:\n".format(self.guild.name, self.channel.name, self.status)
        for m in self.members.keys():
            s+= self.members[m].name + '\n'
        return s