import markdown
import re
import random


_RE_EXTRACT = re.compile('((?:^>![ ]?.*[\n]?)+)', re.MULTILINE)


class SpoilerPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md, holder):
        markdown.preprocessors.Preprocessor.__init__(self, md)
        self._holder = holder

    def run(self, text):
        self._holder.quotes = {}
        def replacement(spoiler):
            part = re.sub(r'^>![ ]?', '', spoiler.group(1), flags=re.MULTILINE)
            id = str(random.randint(0, 0x7FFFFFFF))
            while id in text:
                id = str(random.randint(0, 0x7FFFFFFF))
            self._holder.quotes[id] = part
            return "> %s\n" % id
        text = _RE_EXTRACT.sub(replacement, "\n".join(text)).split("\n")
        return text


class SpoilerPostprocessor(markdown.postprocessors.Postprocessor):
    def __init__(self, md, holder, configs):
        markdown.postprocessors.Postprocessor.__init__(self, md)
        self._holder = holder
        self._md = md
        self._extensions = configs.get('extensions', [])
        self._extension_configs = configs.get('extension_configs', {})

    def run(self, text):
        if not self._holder.quotes:
            return text

        for id, value in self._holder.quotes.iteritems():
            value = markdown.markdown(
                value, extensions=self._extensions, extension_configs=self._extension_configs)
            value = '<blockquote class="markdown-spoiler">%s</blockquote>' % value
            text = re.sub(r'<blockquote>.*?%s.*?</blockquote>' % id, value, text, count=1, flags=re.DOTALL)
        self._holder.quotes = {}
        return text

class SpoilerExtension(markdown.Extension):
    """ Add >! syntax to markdown to mark spoiler blockquotes """
    def __init__(self, configs):
        markdown.Extension.__init__(self)
        self._configs = configs

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('spoiler_quote', SpoilerPreprocessor(md, self), '_end')
        md.postprocessors.add('spoiler_quote', SpoilerPostprocessor(md, self, self._configs), '_end')

def makeExtension(configs={}):
    return SpoilerExtension(configs=dict(configs))
