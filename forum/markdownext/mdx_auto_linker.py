import markdown
import re, socket, logging
from forum.models import Question
from forum import settings

# This approach comes directly from PageDown's Markdown.Converter.js to ensure that the server behaviour is identical to the editor preview
# Any improvement to either should be made in both locations. The two exceptions are allowing for > as a starting character for a URL, by
# the time we're processing these links, there's HTML markup present and question link parsing.
URL_RE = re.compile("(^|\s|>)(https?|ftp)(:\/\/[-A-Z0-9+&@#\/%?=~_|\[\]\(\)!:,\.;]*[-A-Z0-9+&@#\/%=~_|\[\]])($|\W)", re.I);
QUESTION_LINK_RE = re.compile("(https?)(:\/\/" + settings.APP_DOMAIN + "\/questions\/)([0-9]+)", re.I);
AUTO_LINK_RE = re.compile("<((https?|ftp):[^'\">\s]+)>");

EMAIL_LINK_REPLACE_RE = re.compile("(?<= href=\")[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})(?=\")")

def replacer(m):
    url = m.group(1)
    mq = QUESTION_LINK_RE.match(url)
    if mq != None:
        id = mq.group(3)
        question = None
        try:
          question = Question.objects.get(id=id)
        except DoesNotExist:
            logging.error("DoesNotExist exception for question id %s while autolinking" % id)
        if (question != None):
          title = question.title
        else:
          title = url
    else:
        title = url
    return '<a href="%s">%s</a>' % (url, title)

class AutoLinker(markdown.postprocessors.Postprocessor):

    def run(self, text):
        logging.debug("Autolinker called with " + text)

        # Surround any raw links that are valid for auto-linking with <>'s
        text = URL_RE.sub(r"\1<\2\3>\4", text)

        # Substitute an anchor with a replacement title if appropriate
        text = AUTO_LINK_RE.sub(replacer, text)

        # Email substitution
        text = EMAIL_LINK_REPLACE_RE.sub(lambda m: "mailto:%s" % m.group(0), text)

        return text

class AutoLinkerExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.postprocessors['autolinker'] = AutoLinker()

def makeExtension(configs=None):
    return AutoLinkerExtension(configs=configs)

