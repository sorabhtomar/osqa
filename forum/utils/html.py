"""Utilities for working with HTML."""
import bleach
from urllib import quote_plus
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from forum import settings

_ALLOWED_TAGS = ('a', 'abbr', 'acronym', 'address', 'b', 'big',
    'blockquote', 'br', 'caption', 'center', 'cite', 'code', 'col',
    'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em', 'font',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd',
    'li', 'ol', 'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
    'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead',
    'tr', 'tt', 'u', 'ul', 'var')

_ALLOWED_ATTRIBUTES = {
    '*': ('abbr', 'align', 'alt', 'axis', 'border',
        'cellpadding', 'cellspacing', 'char', 'charoff', 'charset', 'cite',
        'cols', 'colspan', 'datetime', 'dir', 'frame', 'headers', 'height',
        'href', 'hreflang', 'hspace', 'lang', 'longdesc', 'name', 'nohref',
        'noshade', 'nowrap', 'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope',
        'span', 'src', 'start', 'summary', 'title', 'type', 'valign', 'vspace',
        'width', 'class'),
}

def sanitize_html(html):
    """Sanitizes an HTML fragment."""
    return bleach.clean(html, tags=_ALLOWED_TAGS, attributes=_ALLOWED_ATTRIBUTES, strip=True)

def cleanup_urls(url):
    return quote_plus(strip_tags(url))

def html2text(s, ignore_tags=(), indent_width=4, page_width=80):
    return mark_safe(bleach.clean(s, tags=ignore_tags, strip=True))

def buildtag(name, content, **attrs):
    return mark_safe('<%s %s>%s</%s>' % (name, " ".join('%s="%s"' % i for i in attrs.items()), unicode(content), name))

def hyperlink(url, title, **attrs):
    return mark_safe('<a href="%s" %s>%s</a>' % (url, " ".join('%s="%s"' % i for i in attrs.items()), title))

def objlink(obj, **attrs):
    return hyperlink(settings.APP_URL + obj.get_absolute_url(), unicode(obj), **attrs)

    


