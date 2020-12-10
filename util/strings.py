import i18n
from i18n import t

i18n.load_path.append('res/strings/')
i18n.set('locale', 'en')
# i18n.set('locale', 'it')
bot_path = 'bot'


def get_string_bot(name, **kwargs):
    return t('{}.{}'.format(bot_path, name), **kwargs)
