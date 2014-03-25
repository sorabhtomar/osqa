import markdown
import re

R_NOFOLLOW = re.compile('<a ')
S_NOFOLLOW = '<a rel="nofollow" '

class NofollowPostprocessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        return R_NOFOLLOW.sub(S_NOFOLLOW, text)

class NofollowExtension(markdown.Extension):
    """ Add nofollow for links to Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('nofollow', NofollowPostprocessor(md), '_end')

def makeExtension(configs={}):
    return NofollowExtension(configs=configs)