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

    items_urls_regexp = \
        r'(http://yuumei.deviantart.com/art/Fisheye-Placebo[\-_\w\d]+)"\s'

    items_titles_regexp = r'class="details"\s?>.*?<b>(.*?)</b>'
