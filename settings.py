# encoding:utf-8
import os.path
import sys
from django.utils import _os

SITE_ID = 1

SECRET_KEY = 'a;::qCl1mfh?avagttOJ;8f5Rr54d,9qy7;o15M2cYO75?OQo51u3LnQ;!8N.:,7'

CACHE_MAX_KEY_LENGTH = 235

MIDDLEWARE_CLASSES = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'forum.middleware.django_cookies.CookiePreHandlerMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'forum.middleware.extended_user.ExtendedUser',
    'forum.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'forum.middleware.request_utils.RequestUtils',
    'forum.middleware.cancel.CancelActionMiddleware',
    'forum.middleware.admin_messages.AdminMessagesMiddleware',
    'forum.middleware.custom_pages.CustomPagesFallbackMiddleware',
    'forum.middleware.django_cookies.CookiePostHandlerMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
    'forum.context.application_settings',
    'django.contrib.messages.context_processors.messages',
    'forum.user_messages.context_processors.user_messages',
    'django.contrib.auth.context_processors.auth',
]

BASEDIR = os.path.dirname(__file__)
SKINDIR = os.path.join(BASEDIR, 'forum', 'skins')

ROOT_URLCONF = 'urls'
APPEND_SLASH = True

TEMPLATE_DIRS = (
    SKINDIR.replace('\\','/'),
)


FILE_UPLOAD_TEMP_DIR = os.path.join(os.path.dirname(__file__), 'tmp').replace('\\','/')
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
 "django.core.files.uploadhandler.TemporaryFileUploadHandler",)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

ALLOW_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ALLOW_MAX_FILE_SIZE = 1024 * 1024

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

STATIC_URL = '/m/'
STATIC_ROOT = os.path.join(BASEDIR, 'static').replace('\\','/')

# User settings
from settings_local import *

def _list_possible_dirs(include_common=False):
    DEFAULT_SKIN_NAME = 'default'
    result = [_os.safe_join(SKINDIR, OSQA_DEFAULT_SKIN)]

    skin_name = OSQA_DEFAULT_SKIN
    while True:
        parent_txt = _os.safe_join(SKINDIR, skin_name, 'parent.txt')
        if not os.path.isfile(parent_txt):
            break
        with open(parent_txt, 'rb') as fp:
            skin_name = fp.readline().decode(FILE_CHARSET).strip()
        p = _os.safe_join(SKINDIR, skin_name)
        if not path.isdir(p):
            break
        result.append(p)

    if OSQA_DEFAULT_SKIN != DEFAULT_SKIN_NAME:
        result.append(_os.safe_join(SKINDIR, DEFAULT_SKIN_NAME))
    if include_common:
        result.append(_os.safe_join(SKINDIR, 'common'))
    return result

STATICFILES_DIRS = [
    ('templates', os.path.join(skin, 'templates')) for skin in _list_possible_dirs()
] + [
    ('public', os.path.join(skin, 'media')) for skin in _list_possible_dirs(include_common=True)
]

template_loaders = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'forum.modules.template_loader.ModulesTemplateLoader',
    'forum.skins.SkinsTemplateLoader',
)
TEMPLATE_LOADERS = list(template_loaders) if DEBUG else [ ('django.template.loaders.cached.Loader', template_loaders) ]

try:
    if len(FORUM_SCRIPT_ALIAS) > 0:
        APP_URL = '%s/%s' % (APP_URL, FORUM_SCRIPT_ALIAS[:-1])
except NameError:
    pass

app_url_split = APP_URL.split("://")

APP_PROTOCOL = app_url_split[0]
APP_DOMAIN = app_url_split[1].split('/')[0]
APP_BASE_URL = '%s://%s' % (APP_PROTOCOL, APP_DOMAIN)

FORCE_SCRIPT_NAME = ''

for path in app_url_split[1].split('/')[1:]:
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME + '/' + path

if FORCE_SCRIPT_NAME.endswith('/'):
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME[:-1]

#Module system initialization
MODULES_PACKAGE = 'forum_modules'
MODULES_FOLDER = os.path.join(SITE_SRC_ROOT, MODULES_PACKAGE)

MODULE_LIST = filter(lambda m: getattr(m, 'CAN_USE', True), [
        __import__('forum_modules.%s' % f, globals(), locals(), ['forum_modules'])
        for f in os.listdir(MODULES_FOLDER)
        if os.path.isdir(os.path.join(MODULES_FOLDER, f)) and
           os.path.exists(os.path.join(MODULES_FOLDER, "%s/__init__.py" % f)) and
           not f in DISABLED_MODULES
])

[MIDDLEWARE_CLASSES.extend(
        ["%s.%s" % (m.__name__, mc) for mc in getattr(m, 'MIDDLEWARE_CLASSES', [])]
                          ) for m in MODULE_LIST]

[TEMPLATE_LOADERS.extend(
        ["%s.%s" % (m.__name__, tl) for tl in getattr(m, 'TEMPLATE_LOADERS', [])]
                          ) for m in MODULE_LIST]


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forum',
]

if DEBUG:
    try:
        import debug_toolbar
        MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        INSTALLED_APPS.append('debug_toolbar')
    except:
        pass

try:
    import south
    INSTALLED_APPS.append('south')
except:
    pass

# Try loading Gunicorn web server
try:
    import gunicorn
    INSTALLED_APPS.append('gunicorn')
except ImportError:
    pass

if not DEBUG:
    try:
        import rosetta
        INSTALLED_APPS.append('rosetta')
    except:
        pass

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]
