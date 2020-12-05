from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# It writes the word on the image with the white cards
# (at the moment it writes only on the first one)
# Problems:
# - you need coordinates for every card
# - you have to re center the text according to its length
# - you can't change the colour of the cards

img = Image.open('../../images/white_cards.png')
draw = ImageDraw.Draw(img)

font = ImageFont.truetype("arial.ttf", 60)
text = "carta1"

W, H = 200, 168  # first card position

# image.size returns a tuple of (width, height) of the image.

w, h = draw.textsize(text)
draw.text((W,H), text, fill="black", font=font)

# you have to re center the text according to its length. Something like below?
# draw.text(((W-w)/2,(H-h)/2), text, fill="black", font=font)

# draw.text((0, 0), text, (255, 255, 255), font=font)
img.save('images/written_white_cards.png')


