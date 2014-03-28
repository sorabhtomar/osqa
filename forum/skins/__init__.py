"""Classes for customizing the staticfiles behavior"""
import collections
import os
from os import path
import shutil

from django.core.files import storage as files_storage
from django.conf import settings
from django.contrib.staticfiles import finders, utils, storage
from django.utils import _os, datastructures


_DEFAULT_SKIN_NAME = 'default'
_TEMPLATE_PREFIX = 'templates'
_MODULE_TEMPLATE_PREFIX = path.join(_TEMPLATE_PREFIX, 'modules')

def _list_dirs(include_common=False):
    result = [_os.safe_join(settings.SKINDIR, settings.OSQA_SKIN)]

    skin_name = settings.OSQA_SKIN
    while True:
        parent_txt = _os.safe_join(settings.SKINDIR, skin_name, 'parent.txt')
        if not path.isfile(parent_txt):
            break
        with open(parent_txt, 'rb') as fp:
            skin_name = fp.readline().decode(settings.FILE_CHARSET).strip()
        p = _os.safe_join(SKINS_FOLDER, skin_name)
        if not path.isdir(p):
            break
        result.append(p)

    if settings.OSQA_SKIN != _DEFAULT_SKIN_NAME:
        result.append(_os.safe_join(settings.SKINDIR, _DEFAULT_SKIN_NAME))
    if include_common:
        result.append(_os.safe_join(settings.SKINDIR, 'common'))
    return result


class _DirStaticFinder(finders.BaseFinder):
    """Abstract class for static files finders which use a list of directories"""

    def find(self, pathname, all=False):
        result = []
        for dir in self._storages.iterkeys():
            abspath = _os.safe_join(dir, pathname)
            if not path.isfile(abspath):
                continue
            if not all:
                return abspath
            result.add(abspath)
        return result

    def list(self, ignore_patterns):
        for storage in self._storages.itervalues():
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage


class _SkinDirStaticFinder(_DirStaticFinder):
    """Finds files in a subdirectory of the skin repsecting parent relationships"""

    def __init__(self, dirname, prefix, *args, **kwargs):
        super(_SkinDirStaticFinder, self).__init__(*args, **kwargs)
        possible_dirs = [
            path.join(d, dirname)
            for d in _list_dirs() if path.isdir(path.join(d, dirname))]
        self._storages = collections.OrderedDict()
        for d in possible_dirs:
            store = files_storage.FileSystemStorage(location=d)
            if prefix:
                store.prefix = prefix
            self._storages[d] = store


class SkinsTemplateFinder(_SkinDirStaticFinder):
    def __init__(self, *args, **kwargs):
        super(SkinsTemplateFinder, self).__init__('templates', _TEMPLATE_PREFIX, *args, **kwargs)


class SkinsMediaFinder(_SkinDirStaticFinder):
    def __init__(self, *args, **kwargs):
        super(SkinsMediaFinder, self).__init__('media', None, *args, **kwargs)


class ModulesTemplateFinder(_DirStaticFinder):
    """Finds the templates from the modules"""

    def __init__(self, *args, **kwargs):
        super(ModulesTemplateFinder, self).__init__(*args, **kwargs)
        self._storages = collections.OrderedDict()
        for m in settings.MODULE_LIST:
            module_dir = path.dirname(m.__file__)
            template_dir = path.join(module_dir, 'templates')
            if not path.isdir(template_dir):
                continue
            store = files_storage.FileSystemStorage(location=template_dir)
            store.prefix = path.join(_MODULE_TEMPLATE_PREFIX, path.basename(module_dir))
            self._storages[template_dir] = store


class TemplateSeparatorStorage(storage.StaticFilesStorage):
    """A storage for staticfiles which separates "templates" from "public" files"""

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return
        template_prefix = '%s%s' % (_TEMPLATE_PREFIX, os.sep)
        template_dir = path.abspath(path.join(settings.STATIC_ROOT, '..', 'templates'))
        if path.isdir(template_dir):
            shutil.rmtree(template_dir)

        for name, v in paths.iteritems():
            if not name.startswith(template_prefix):
                yield name, name, False
                continue

            source_path = path.join(settings.STATIC_ROOT, name)
            dest_path = path.join(template_dir, name[len(template_prefix):])
            try:
                os.makedirs(path.dirname(dest_path))
            except OSError:
                pass
            os.rename(source_path, dest_path)
            yield name, dest_path, True

        shutil.rmtree(path.join(settings.STATIC_ROOT, 'templates'), ignore_errors=True)
