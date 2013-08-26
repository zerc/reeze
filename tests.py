#!venv/bin/python
# coding: utf-8
import re
import os
import unittest

import base
import backends


class TestMixin(object):
    def __init__(self, *args, **kwargs):
        self.prefix = self.__class__.__name__.lower().split('test')[0]
        self.set_less_items_filename()
        super(TestMixin, self).__init__(*args, **kwargs)

    @property
    def raw_data(self):
        with open(os.path.join('for_tests', self.tmp_filename), 'r') as r:
            return r.read()

    def set_items_filename(self):
        self.tmp_filename = '%s_items.html' % self.prefix

    def set_less_items_filename(self):
        self.tmp_filename = '%s_less_items.html' % self.prefix


## TODO: do it dynamic
class GigantsTestBackend(TestMixin, base.get_backend('gigants')):
    pass


class DeviantTestBackend(TestMixin, base.get_backend('deviant')):
    pass


class BaseTestMixin(object):
    def setUp(self):
        if os.path.exists(self.backend.cache_filename):
            os.remove(self.backend.cache_filename)

    def test_items(self):
        for item in self.backend.items:
            self.assertIsInstance(item, base.BaseItem, "Invalid item class")

        self.assertNotEqual(item, None)

    def test_new_items(self):
        self.backend.save()
        self.backend.set_items_filename()

        new_items = self.backend.new_items

        self.assertEqual(1, len(new_items), "Invalid new items count")
        self.assertEqual(
            new_items[0].id, self.new_item_id, "Invalid new item id")

        self.assertIsInstance(new_items, list, "Invalid new items type")
        self.assertIsInstance(
            new_items[0], base.BaseItem, "Invalid new item class")


class GigantTest(BaseTestMixin, unittest.TestCase):
    backend = GigantsTestBackend()
    new_item_id = 2402


class DeviantTest(BaseTestMixin, unittest.TestCase):
    backend = DeviantTestBackend()
    new_item_id = 359809568


if __name__ == "__main__":
    unittest.main()
