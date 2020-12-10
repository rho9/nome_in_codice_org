from util.strings import get_string_bot as _


class Team:
    """A class to represent the team in the game.

    """
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.master = None
        self.members = dict()

    def set_master(self, member):
        """Sets the master in the team

        """
        self.join(member)
        self.master = member

    def print_status(self):
        """returns the string of the status of the team

        """

        s = 'Team {}\n{} (Master)\n'.format(self.name, self.master)
        for m in self.members.keys():
            s += self.members[m].name + '\n'
        return s

    def print_members(self):
        s = _('team', team=self.name) + '\n'
        if self.master is not None:
            s += self.master.name + ' ({})\n'.format(_('master'))
        for m in self.members.keys():
            if self.master is None or m != self.master.id:
                s += self.members[m].name + ' ({})\n'.format(_('spy'))
        return s+'\n'

    def join(self, member):
        self.members[member.id] = member

    def leave(self, member):
        self.members.pop(member.id, None)
        if self.master.id == member.id:
            self.master = None
