# coding: utf-8
"""
Example of backend file
"""
import re
import base


class ExampleItem(base.BaseItem):
    @base.cached_property
    def id(self):
        """
        Genereated unique id for per item
        """
        return int(''.join(re.findall('\d+', self.url)))


class Example(base.BaseBackend):
    item_cls = ExampleItem

    url = "Place where stored items"

    items_urls_regexp = re.compile(
        "Compiled regexp items urls"
        base.RE_FLAGS)

    items_titles_regexp = re.compile(
        "Compiled regexp for item titles", base.RE_FLAGS)
