import random
from game.word import WordTable
from game.image_generator import ImageGenerator

words_table = WordTable()
words_table.generate_words("tag")
print(words_table.print_status())
# reveal 10 cards randomly
i = 10
while i > 0:
    words_table.words[random.randint(0, 24)].reveal()
    i -= 1
img_gen = ImageGenerator()
img_gen.generate(words_table.words, False)
