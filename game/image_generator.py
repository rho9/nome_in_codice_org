from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
from game import colorgame


class ImageGenerator:
    """
    A class to generate an image from a list of Word objects
    """

    def __init__(self):
        self.col_num = 5
        self.space_btw_cards = 30
        self.font = ImageFont.truetype("arial.ttf", 25)
        self.master = None

    def generate(self, words, master):
        """
        This function generate the path containing the grid with the cards

        :param words: list of Word objects
        :param master: boolean to generate the image according to the role
        :return: image path
        """
        self.master = master
        background = self.create_bg('res/images/cards/white_card.png', words)
        for word in words:
            pos = words.index(word)
            if word.revealed:
                background = self.add_card(background, word.image_path, pos)
            else:
                if self.master:
                    # choose the color of the card
                    if word.color == colorgame.ColorGame.RED:
                        card_path = 'res/images/cards/red_card.png'
                    elif word.color == colorgame.ColorGame.BLUE:
                        card_path = 'res/images/cards/blue_card.png'
                    elif word.color == colorgame.ColorGame.WHITE:
                        card_path = 'res/images/cards/white_card.png'
                    else:
                        card_path = 'res/images/cards/black_card.png'
                else:
                    card_path = 'res/images/cards/white_card.png'
                written_card_path = self.write_on_card(card_path, word)
                background = self.add_card(background, written_card_path, pos)
        background.save('res/images/grid.png')
        os.remove('res/images/cards/temp/written_card.png')
        return 'res/images/grid.png'

    def create_bg(self, img_path, words):
        """
        This function creates the background of the image

        :param img_path: path of the image to set the dimensions
        :param words: list of Word objects
        :return: background image
        """
        with Image.open(img_path) as img:
            img_w, img_h = img.size

        # compute background width
        bg_width = self.col_num * (img_w + self.space_btw_cards) + self.space_btw_cards

        # compute background height
        row_num = len(words) // self.col_num
        if len(words) % self.col_num != 0:
            row_num = + 1
        bg_height = row_num * (img_h + self.space_btw_cards) + self.space_btw_cards

        # Image constructor: mode, size (width, height in pixels), color.
        background = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255, 255))
        return background

    def write_on_card(self, card_path, word):
        """
        This function writes the word on the card

        :param card_path: the card path to write on
        :param word: the word to write
        :return: the path of the written card
        """
        with Image.open(card_path) as img:
            draw = ImageDraw.Draw(img)
            # calculate where to place the word inside the white space of the card
            (word_width, word_height), (offset_x, offset_y) = self.font.font.getsize(word.name)
            # coordinates of the white space
            x_left = 18
            x_right = 160
            y_up = 65
            y_down = 98
            # dimension of the white space
            white_space_width = x_right - x_left
            white_space_height = y_down - y_up
            # white space that remains free
            free_space_x = white_space_width - word_width
            free_space_y = white_space_height - 23
            # 23 and not word_height because sometimes it is 18 and sometimes it is 23
            # and then the words are on different planes and they suck
            # (maybe if there is a letter going down the height increases).
            # coordinates of the beginning of the word
            word_x_pos = x_left + (free_space_x // 2)
            word_y_pos = y_up + (free_space_y // 2)

            # choose the color of the text
            if self.master and word.color == colorgame.ColorGame.ASSASSIN:
                font_color = "white"
            else:
                font_color = "black"
            draw.text((word_x_pos, word_y_pos), word.name, fill=font_color, font=self.font)
            img.save('res/images/cards/temp/written_card.png')
        return 'res/images/cards/temp/written_card.png'

    def add_card(self, background, card_path, pos):
        """
        This function add the word to the background

        :param background: image on which to add the card
        :param card_path: the card path to add to the background
        :param pos: the position of the word in the background
        :return: the updated image of the background
        """
        with Image.open(card_path) as img:
            img_w, img_h = img.size
            # top-left corner coordinates of the card in the background
            card_x = (pos % self.col_num) * img_w + (pos % self.col_num + 1) * self.space_btw_cards
            card_y = (pos // self.col_num) * img_h + ((pos // self.col_num) + 1) * self.space_btw_cards
            offset = (card_x, card_y)
            background.paste(img, offset)
        return background
