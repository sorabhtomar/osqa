import json

from django.core.management.base import NoArgsCommand
from forum import settings
from forum.settings import BaseSetting

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        print "/*"
        changed_settings = {}
        for k in dir(settings):
            attr = getattr(settings, k)
            if not isinstance(attr, BaseSetting):
                continue
            if attr.value == attr.default:
                print "- %s is set to the default value" % k
                continue

            if attr.field_context:
                print "\n- %s" % k
                label = attr.field_context.get('label')
                if label:
                    print "  %s" % unicode(label).strip()
                help_text = attr.field_context.get('help_text')
                if help_text:
                    print "  %s" % unicode(help_text).strip()
            changed_settings[k] = attr.value
        print "*/"
        print json.dumps(changed_settings, sort_keys=True,
            indent=4, separators=(',', ': '))
