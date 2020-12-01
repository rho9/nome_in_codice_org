from game.colorgame import ColorGame


class Word():
    """A class to represent a word in the game

    """

    def __init__(self, name):
        self.name = name #: name
        self.color = ColorGame.NONE #: color of the word
