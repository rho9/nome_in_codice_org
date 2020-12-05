from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# remember to use 'with Image.open('test.jpg') as img:' to avoid memory disaster
img = Image.open('../../images/white_card.png', 'r')
draw = ImageDraw.Draw(img)
img_w, img_h = img.size

cards_number = 5
space = 30
bg_width = cards_number * (img_w + space) + space
bg_height = 1700
# Image constructor: mode, size (width, height in pixels), color.
background = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255, 255))

font = ImageFont.truetype("arial.ttf", 50)
word_list = ["carta1", "carta22222", "carta33", "carta4", "carta5"]

# row
for word in word_list:
    img = Image.open('../../images/white_card.png', 'r')
    draw = ImageDraw.Draw(img)

    # calculate where to place the word inside the white space of the card
    (word_width, baseline), (offset_x, offset_y) = font.font.getsize(word)
    # print("word_width:", word_width)
    # print("baseline:", baseline)
    # print("offset_x:", offset_x)
    # print("offset_y:", offset_y)
    # pixel number in which the white space in the card starts and ends
    start_pixel = 40
    end_pixel = 335
    available_space = end_pixel-start_pixel
    free_space = available_space - word_width
    # W, H: top left position of the word in the white space of the card
    W, H = (40+(free_space//2)), 142

    draw.text((W,H), word, fill="black", font=font)
    pos = word_list.index(word)
    offset = (pos * img_w +(pos+1)*30, 30)  # pixel coordinates
    background.paste(img, offset)

word_list = ["carta6", "carta7", "carta8", "carta9", "carta10"]

# second column
for word in word_list:
    img = Image.open('../../images/white_card.png', 'r')
    draw = ImageDraw.Draw(img)
    draw.text((W, H), word, fill="black", font=font)
    pos = word_list.index(word)
    offset = (30, pos * img_h + (pos + 1) * 30)  # pixel coordinates
    background.paste(img, offset)

background.save('images/grid.png')