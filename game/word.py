from game.colorgame import ColorGame
from game.database import Database
import random
from util.exception import NotAllowedCommand
from util.strings import get_string_bot as _

class Word():
    """A class to represent a word in the game

    """

    def __init__(self, name, color):
        self.name = name #: name
        self.color = color #: color of the word
        self.revealed = False

    """private method to reveal the word

    """
    def show(self):
        if self.revealed:
            raise NotAllowedCommand(_('error_word_show'))
        else:
            self.revealed = True

    def print_status(self):
        color = ''
        if self.color == ColorGame.RED:
            color = ':red_circle:'
        elif self.color == ColorGame.BLUE:
            color = ':blue_circle:'
        elif self.color == ColorGame.WHITE:
            color = ':white_circle:'
        else:
            color = ':skull:'

        if self.revealed:
            bold = '__'
        else:
            bold = ''

        return "{}{}{}{}".format(bold,self.name,color,bold)



class WordTable():
    """A class that represent the grid of the game

        """

    def __init__(self):
        self.size = 25
        self.words = []
        self.number_red = 9
        self.number_blue = 8
        self.number_assassin = 1
        self.number_white = self.size - (self.number_red + self.number_blue + self.number_assassin)


    def generate_words(self, tag):
        """Generate the word from the database

            """
        db = Database()
        listOfWord = db.get_words_by_tag(tag)
        if len(listOfWord) < self.size:
            raise NotAllowedCommand(_('error_missing_words', tag = tag))
        self.words_str = random.sample(listOfWord, self.size)
        self.red_words = random.sample(self.words_str, self.number_red)

        red_set = set(self.red_words)
        self.blue_words = random.sample([x for x in self.words_str if x not in red_set], self.number_blue)

        blue_set = set(self.blue_words)
        self.assassin_words = random.sample([x for x in self.words_str if x not in red_set and x not in blue_set], self.number_assassin)
        self.white_words = [x for x in self.words_str if x not in red_set and x not in blue_set and x not in self.assassin_words]
        self.create_grid()

    def create_grid(self):
        """Create the structure with words

            """
        self.words = []
        for w in self.words_str:
            if w in self.red_words:
                self.words.append(Word(w,ColorGame.RED))
            elif w in self.blue_words:
                self.words.append(Word(w,ColorGame.BLUE))
            elif w in self.white_words:
                self.words.append(Word(w,ColorGame.WHITE))
            else:
                self.words.append(Word(w,ColorGame.ASSASSIN))

    def show(self, string):
        """Reveal the word

            """
        for w in self.words:
            if w.name.lower() == string.lower():
                w.show()
                return True, w.color
        return False, None

    def get_red_point(self):
        """Count the red card revealed

            """
        return [(lambda x:x.revealed)(w) for w in self.words if w.color == ColorGame.RED].count(True)

    def get_blue_point(self):
        """Count the blue card revealed

            """
        return [(lambda x:x.revealed)(w) for w in self.words if w.color == ColorGame.BLUE].count(True)

    def print_status(self):
        num = 5
        s = 'Grid:\n'
        for w in self.words:
            s += w.print_status() + ' - '
            num -= 1
            if num == 0:
                s += '\n'
                num = 5
        s+= 'Word guessed\nRed team: {}\nBlue team:{}\n'.format(self.get_red_point(),self.get_blue_point())
        return s