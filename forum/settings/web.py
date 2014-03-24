import os.path

from base import Setting, SettingSet
from forms import ImageFormWidget

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea

WEB_SET = SettingSet('web', _('Web settings'), _("Web settings for the application"))

ENDLESS_PAGINATION = Setting('ENDLESS_PAGINATION', True, WEB_SET, dict(
label = _("Use endless pagination"),
help_text = _("Check if you want to use endless, automatically loading pagination instead of legacy paging (experimental)."),
required=False))

PJAX_TIMEOUT = Setting('PJAX_TIMEOUT', 1500, WEB_SET, dict(
label = _("PJAX request timeout"),
help_text = _("Value in milliseconds used to determine how long PJAX will wait for an RPC request before falling back to a standard request."),
required=False))
