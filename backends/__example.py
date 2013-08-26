# coding: utf-8
import re
import base


## deviantart
class DeviantItem(base.BaseItem):
    @base.cached_property
    def id(self):
        return int(''.join(re.findall('\d+', self.url)))


class Deviant(base.BaseBackend):
    item_cls = DeviantItem

    url = 'http://yuumei.deviantart.com/gallery/'

    items_urls_regexp = re.compile(
        r'(http://yuumei.deviantart.com/art/Fisheye-Placebo[\-_\w\d]+)"\s',
        base.RE_FLAGS)

    items_titles_regexp = re.compile(
        r'class="details"\s?>.*?<b>(.*?)</b>', base.RE_FLAGS)
