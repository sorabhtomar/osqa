from os import path
import logging

from django.core.cache.backends import locmem
from django.conf import settings
from django.utils import _os
from django.template.loaders import filesystem

SKINS_FOLDER = path.dirname(__file__)
DEFAULT_SKIN_NAME = 'default'

def _list_dirs(include_common=False):
    result = [_os.safe_join(SKINS_FOLDER, settings.OSQA_DEFAULT_SKIN)]

    skin_name = settings.OSQA_DEFAULT_SKIN
    while True:
        parent_txt = _os.safe_join(SKINS_FOLDER, skin_name, 'parent.txt')
        if not path.isfile(parent_txt):
            break
        with open(parent_txt, 'rb') as fp:
            skin_name = fp.readline().decode(settings.FILE_CHARSET).strip()
        p = _os.safe_join(SKINS_FOLDER, skin_name)
        if not path.isdir(p):
            break
        result.append(p)

    if settings.OSQA_DEFAULT_SKIN != DEFAULT_SKIN_NAME:
        result.append(_os.safe_join(SKINS_FOLDER, DEFAULT_SKIN_NAME))
    if include_common:
        result.append(_os.safe_join(SKINS_FOLDER, 'common'))
    return result


TEMPLATE_DIRS = _list_dirs()
MEDIA_DIRS = _list_dirs(include_common=True)
SKIN_TEMPLATES_FOLDER = 'templates'
FORCE_DEFAULT_PREFIX = "%s/" % DEFAULT_SKIN_NAME


class SkinsTemplateLoader(filesystem.Loader):
    def load_template_source(self, name, dirs=None):
        name = '%s/%s' % (SKIN_TEMPLATES_FOLDER, name)
        if name.startswith(FORCE_DEFAULT_PREFIX):
            name = name[len(FORCE_DEFAULT_PREFIX):]
            dirs = [_os.safe_join(SKINS_FOLDER, DEFAULT_SKIN_NAME, SKIN_TEMPLATES_FOLDER)]
        else:
            dirs = TEMPLATE_DIRS
        return super(SkinsTemplateLoader, self).load_template_source(name, dirs)


__media_src_cache = locmem.LocMemCache('osqa-media-src-cache', {})

def find_media_source(url):
    """returns url prefixed with the skin name
    of the first skin that contains the file 
    directories are searched in this order:
    settings.OSQA_DEFAULT_SKIN, then 'default', then 'common'
    if file is not found - returns None
    and logs an error message
    """
    while url[0] == '/': url = url[1:]

    if not settings.DEBUG:
        cached = __media_src_cache.get(url)
        if cached:
            return cached

    for skin_path in MEDIA_DIRS:
        filename = path.join(skin_path, url)
        if path.isfile(filename):
            result = filename[len(SKINS_FOLDER)+1:]
            if not settings.DEBUG:
                __media_src_cache.set(url, result)
            return result

    logging.error('could not find media for %s' % url)
    return None
