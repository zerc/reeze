# coding: utf-8
import re
import base


## anilibria
class GigantItem(base.BaseItem):
    @base.cached_property
    def id(self):
        return int(re.findall('(\d+)', self.url)[0])


class Gigants(base.BaseBackend):
    item_cls = GigantItem

    url = 'http://www.anilibria.tv' + \
        '/release/shingeki-no-kyojin-vtorzhenie-gigantov'

    items_urls_regexp = \
        r'(/wp-content/plugins/tracker-frontend/get.php\?id=\d+)'

    items_titles_regexp = r"id='linked'>(.*?)<"
