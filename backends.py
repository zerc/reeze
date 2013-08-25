#!venv/bin/python
# coding: utf-8
import re
import sys
import base


## anilibria
class GigantItem(base.BaseItem):
    @base.cached_property
    def id(self):
        return int(re.findall('(\d+)', self.url)[0])


class Gigants(base.BaseBackend):
    __metaclass__ = base.Registered

    item_cls = GigantItem

    url = 'http://www.anilibria.tv' + \
        '/release/shingeki-no-kyojin-vtorzhenie-gigantov'

    items_urls_regexp = re.compile(
        r'(/wp-content/plugins/tracker-frontend/get.php\?id=\d+)',
        base.RE_FLAGS)

    items_titles_regexp = re.compile(r"id='linked'>(.*?)<", base.RE_FLAGS)


## deviantart
class DeviantItem(GigantItem):
    @base.cached_property
    def id(self):
        return int(''.join(re.findall('\d+', self.url)))


class Deviant(base.BaseBackend):
    __metaclass__ = base.Registered

    item_cls = DeviantItem

    url = 'http://yuumei.deviantart.com/gallery/'

    items_urls_regexp = re.compile(
        r'(http://yuumei.deviantart.com/art/Fisheye-Placebo[\-_\w\d]+)"\s',
        base.RE_FLAGS)

    items_titles_regexp = re.compile(
        r'class="details"\s?>.*?<b>(.*?)</b>', base.RE_FLAGS)
