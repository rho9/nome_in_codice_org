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

class ActionResult(Enum):
    '''
    A class to represent the result of the action show.
    '''

    GUESS = 1 #: returned when the player guess the word
    NOT_GUESS = 2 #: returned when the player didn't guess the word
    FINISH = 3 #: returned when the player chose the assassin, guess the word and win or not guessed and lose

class Match():
    """A class to represent the match. It stores the guild, the channel, the list of members, the status and if the status of
    the match is Status.PLAY also the StartedMatch object.

       """
    def __init__(self, guild, channel):
        self.guild = guild
        self.channel = channel
        self.members = dict()
        self.status = Status.NOT_STARTED
        self.team_red = None
        self.team_blue = None
        self.winner = None

    def verify_victory_condition(self):
        if self.grid_table.get_red_point() == self.grid_table.number_red:
            return self.team_red
        elif self.grid_table.get_blue_point() == self.grid_table.number_blue:
            return self.team_blue
        else:
            return None

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
                self.leave_master(member)
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
            self.team_red = Team(ColorGame.RED, 'Red')
            self.team_blue = Team(ColorGame.BLUE, 'Blue')


    def play(self, tag):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand('The match is not started')
        elif self.status == Status.PLAY:
            raise NotAllowedCommand('The match is already started and in progress')
        elif not self.has_masters():
            raise NotAllowedCommand('We need two masters for play the game')
        else:
            self.status = Status.PLAY
            self.grid_table = WordTable()
            self.grid_table.generate_words(tag)
            self.current_turn = self.team_red
            self.next_turn = self.team_blue

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
            s += 'current turn: {} team\n'.format(self.current_turn.name)
            s += self.grid_table.print_status()
        if s == '':
            return 'no match found'
        return s

    def join_as_master(self, member):
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
            if member.id not in self.members.keys():
                self.join(member)
            return self.join_team(member)

    def has_masters(self):
        return self.team_red.master != None and self.team_blue.master != None

    def leave_master(self, member):
        if self.team_red.master == member:
            self.team_red.master = None
        if self.team_blue.master == member:
            self.team_blue.master = None

    def join_team(self, member):
        if self.team_red.master == None:
            self.team_red.set_master(member)
            return self.team_red.name
        elif self.team_blue.master == None:
            self.team_blue.set_master(member)
            return self.team_blue.name
        else:
            raise NotAllowedCommand('Master is already set')

    def show(self, member, word):
        if self.status == Status.PLAY:
            if self.current_turn.master.id == member.id:
                found, color = self.grid_table.show(word)
                if not found:
                    raise NotAllowedCommand('{} is not found'.format(word))
                elif color == ColorGame.ASSASSIN:
                    self.status = Status.STOPPED
                    self.winner = self.next_turn

                    return ActionResult.FINISH
                elif self.verify_victory_condition() == None:
                    if color != self.current_turn.color:
                        self.current_turn, self.next_turn = self.next_turn, self.current_turn
                        return ActionResult.NOT_GUESS
                    else:
                        return ActionResult.GUESS
                else:
                    self.winner = self.verify_victory_condition()
                    self.status = Status.STOPPED
                    return ActionResult.FINISH
            else:
                raise NotAllowedCommand('Only the {} team\'s master can write the word'.format(self.current_turn.name))
        else:
            raise NotAllowedCommand('The match is not started')

    def pass_turn(self, member):
        if self.status == Status.PLAY:
            if member.id == self.current_turn.master.id:
                self.current_turn, self.next_turn = self.next_turn, self.current_turn
            else:
                raise NotAllowedCommand("Only the master of the {} team can give this command".format(self.current_turn.master.name))
        else:
            raise NotAllowedCommand("The match is not started")