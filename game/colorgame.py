from enum import Enum

class ColorGame(Enum):
    """A class to represent the possible color in the game.

    """
    RED = 1 #: Red agent
    BLUE = 2 #: Blue agent
    WHITE = 3 #: Neutral agent
    ASSASSIN = 4 #: Black agent
    NONE = 5 #: NONE is the color assumed by words **before** the game generates the schema.