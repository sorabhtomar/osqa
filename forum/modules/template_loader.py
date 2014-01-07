import re
from os import path

from django.conf import settings
from django.utils._os import safe_join
from django.template.loaders import filesystem

from forum import skins


MODULES_TEMPLATE_PREFIX = 'modules/'
NO_OVERRIDE_TEMPLATE_PREFIX = 'no_override/'
MODULES_TEMPLATE_FOLDER = 'templates'
MODULES_TEMPLATE_OVERRIDES_FOLDER = 'template_overrides'

TEMPLATE_OVERRIDE_LOOKUP_PATHS = [f for f in [
        safe_join(path.dirname(m.__file__), MODULES_TEMPLATE_OVERRIDES_FOLDER) for m in settings.MODULE_LIST
    ] if path.exists(f)
]


class ModulesTemplateLoader(filesystem.Loader):

    __MODULES_RE = re.compile('^%s(\w+)\/(.*)$' % MODULES_TEMPLATE_PREFIX)
    __SKIN_TEMPLATE_LOADER = skins.SkinsTemplateLoader()

    def load_template_source(self, name, dirs=None):
        if name.startswith(MODULES_TEMPLATE_PREFIX):
            match = self.__MODULES_RE.search(name)
            name = match.group(2)
            dirs = [safe_join(settings.MODULES_FOLDER, match.group(1), MODULES_TEMPLATE_FOLDER)]
            return super(ModulesTemplateLoader, self).load_template_source(name, dirs)
        elif name.startswith(NO_OVERRIDE_TEMPLATE_PREFIX):
            name = name[len(NO_OVERRIDE_TEMPLATE_PREFIX):]
            return self.__SKIN_TEMPLATE_LOADER.load_template_source(name, dirs)
        else:
            return super(ModulesTemplateLoader, self).load_template_source(name, TEMPLATE_OVERRIDE_LOOKUP_PATHS)
