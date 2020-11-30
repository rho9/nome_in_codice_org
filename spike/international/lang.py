import i18n
from i18n import t as _
i18n.load_path.append('./')

i18n.set('locale', 'en')
print(_('foo.hi'))
print(_('foo.hin', name='Bob'))
i18n.set('locale', 'it')
print(_('foo.hi'))
print(_('foo.hin', name='Bob'))
