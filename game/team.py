class Team():
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.master = None
        self.current_turn = False
        self.members = dict()

    def set_master(self, member):
        self.master = member

    def print_status(self):
        s = 'Team {}\n{} (Master)\n'.format(self.name, self.master)
        for m in self.members.keys():
            s =+ self.members[m].name + '\n'
        return s