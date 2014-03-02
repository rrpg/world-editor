import gettext
from core import config

_ = gettext.translation('message', config.localesDir).ugettext
