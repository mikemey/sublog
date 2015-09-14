from markdown import util

import markdown
from markdown.inlinepatterns import LinkPattern, Pattern, IMAGE_LINK_RE, LINK_RE, ImagePattern


class ImageLinkPattern(Pattern):
    def __init__(self, mdi):
        Pattern.__init__(self, IMAGE_LINK_RE, mdi)
        self.link = LinkPattern(LINK_RE, mdi)
        self.image = ImagePattern(IMAGE_LINK_RE, mdi)

    def handleMatch(self, m):
        img = self.image.handleMatch(m)
        img.set('style', 'max-width:100%;')

        anchor = util.etree.Element("a")
        anchor.set('href', img.get('src'))
        anchor.set('target', '_blank')
        anchor.append(img)
        return anchor


class ImageLinkExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["image_link"] = ImageLinkPattern(md)
