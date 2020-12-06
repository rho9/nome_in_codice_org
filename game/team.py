class Team():
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
        self.master = member

    def print_status(self):
        """returns the string of the status of the team

        """

        s = 'Team {}\n{} (Master)\n'.format(self.name, self.master)
        for m in self.members.keys():
            s =+ self.members[m].name + '\n'
        return s