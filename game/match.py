from enum import Enum
import random

from game.colorgame import ColorGame
from game.team import Team
from game.word import WordTable
from util.exception import NotAllowedCommand
from util.strings import get_string_bot as _


class Status(Enum):
    """A class to represent the possible status for a match

       """
    NOT_STARTED = 1  #: it is a not joinable match just instantiated
    JOINABLE = 2  #: it is a match in which players can join in.
    PLAY = 3  #: it is a match started and players can't join in
    STOPPED = 4  #: it is a match stopped


class ActionResult(Enum):
    """A class to represent the result of the action show.

    """

    GUESS = 1  #: returned when the player guess the word
    NOT_GUESS = 2  #: returned when the player didn't guess the word
    FINISH = 3  #: returned when the player chose the assassin, guess the word and win or not guessed and lose


class Match:
    """A class to represent the match. It stores the guild, the channel, the list of members, the status and if the stat
    us of the match is Status.PLAY also the StartedMatch object.

       """
    def __init__(self, guild, channel):
        self.guild = guild
        self.channel = channel
        self.status = Status.NOT_STARTED
        self.team_red = None
        self.team_blue = None
        self.winner = None
        self.grid_table = None
        self.current_turn = None
        self.next_turn = None

    def verify_victory_condition(self):
        if self.grid_table.get_red_point() == self.grid_table.number_red:
            return self.team_red
        elif self.grid_table.get_blue_point() == self.grid_table.number_blue:
            return self.team_blue
        else:
            return None

    def get_team_member(self, member):
        if member.id in self.team_red.members.keys():
            return self.team_red
        if member.id in self.team_blue.members.keys():
            return self.team_blue
        return None

    def join(self, member):
        if self.status != Status.JOINABLE:
            raise NotAllowedCommand(_('error_joinable'))
        if self.get_team_member(member) is None:
            self.auto_join(member)
        else:
            raise NotAllowedCommand(_('error_already_joined', team=self.get_team_member(member).name))

    def leave(self, member):
        if self.status != Status.JOINABLE:
            raise NotAllowedCommand(_('error_joinable'))
        team = self.get_team_member(member)
        if team is not None:
            team.leave(member)
        else:
            raise NotAllowedCommand(_('error_not_join'))

    def start(self):
        if self.status == Status.JOINABLE:
            raise NotAllowedCommand(_('error_started'))
        else:
            self.status = Status.JOINABLE
            self.team_red = Team(ColorGame.RED, 'Red')
            self.team_blue = Team(ColorGame.BLUE, 'Blue')

    def play(self, tag):
        if self.status != Status.JOINABLE:
            raise NotAllowedCommand(_('error_joinable'))
        elif not self.has_masters():
            raise NotAllowedCommand(_('error_need_two_master'))
        else:
            self.status = Status.PLAY
            self.grid_table = WordTable()
            self.grid_table.generate_words(tag)
            self.current_turn = self.team_red
            self.next_turn = self.team_blue

    def stop(self):
        if self.status == Status.NOT_STARTED or self.status == Status.STOPPED:
            raise NotAllowedCommand(_('error_not_started'))
        else:
            self.status = Status.STOPPED

    def print_members(self):
        s = _('members') + ':\n'
        s += self.team_red.print_members()
        s += self.team_blue.print_members()
        return s

    def print_status(self):
        s = "Guild id: {}, channel id: {}, status: {} \n".format(self.guild.name, self.channel.name, self.status)

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
            raise NotAllowedCommand(_('error_joinable'))
        else:
            return self.join_team_as_master(member)

    def has_masters(self):
        return self.team_red.master is not None and self.team_blue.master is not None

    def join_team_as_master(self, member):
        if self.team_red.master is not None and self.team_blue.master is not None:
            raise NotAllowedCommand(_('error_master_already_set'))
        if self.team_red.master is None and member.id not in self.team_blue.members.keys():
            self.team_red.set_master(member)
            return self.team_red.name
        elif self.team_blue.master is None and member.id not in self.team_red.members.keys():
            self.team_blue.set_master(member)
            return self.team_blue.name
        else:
            raise NotAllowedCommand(_('error_master_other_team'))

    def show(self, member, word):
        if self.status == Status.PLAY:
            if self.current_turn.master.id == member.id:
                found, color = self.grid_table.show(word)
                if not found:
                    raise NotAllowedCommand(_('error_word_not_found', word=word))
                elif color == ColorGame.ASSASSIN:
                    self.status = Status.STOPPED
                    self.winner = self.next_turn

                    return ActionResult.FINISH
                elif self.verify_victory_condition() is None:
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
                raise NotAllowedCommand(_('error_team_not_allowed', team=self.current_turn.name))
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def pass_turn(self, member):
        if self.status == Status.PLAY:
            if member.id in self.current_turn.members.keys():
                self.current_turn, self.next_turn = self.next_turn, self.current_turn
            else:
                raise NotAllowedCommand(_('error_team_not_allowed', team=self.current_turn.name))
        else:
            raise NotAllowedCommand(_('error_not_started'))

    def auto_join(self, member):
        team = self.choose_team()
        team.join(member)

    def choose_team(self):
        if len(self.team_red.members) < len(self.team_blue.members):
            return self.team_red
        elif len(self.team_red.members) > len(self.team_blue.members):
            return self.team_blue
        else:
            return random.sample([self.team_blue, self.team_red], 1)[0]

    def change_team(self, member):
        if self.status != Status.JOINABLE:
            raise NotAllowedCommand(_('error_joinable'))
        if member.id in self.team_red.members.keys():
            self.team_red.leave(member)
            self.team_blue.join(member)
        elif member.id in self.team_blue.members.keys():
            self.team_blue.leave(member)
            self.team_red.join(member)
        else:
            raise NotAllowedCommand(_('error_not_join'))
