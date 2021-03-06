#!venv/bin/python
# coding: utf-8
import re
import os
import unittest

import run
import base
import backends
import actions


class TestMixin(object):
    def __init__(self, *args, **kwargs):
        self.prefix = self.__class__.__name__.lower().split('test')[0]
        self.set_less_items_filename()
        super(TestMixin, self).__init__(*args, **kwargs)

    @property
    def raw_data(self):
        with open(os.path.join('for_tests', self.tmp_filename), 'r') as r:
            return r.read().decode('utf-8')

    def set_items_filename(self):
        self.tmp_filename = '%s_items.html' % self.prefix

    def set_less_items_filename(self):
        self.tmp_filename = '%s_less_items.html' % self.prefix


## TODO: auto do it
class GigantsTestBackend(TestMixin, base.BACKENDS.get('gigants').__class__):
    pass


class DeviantTestBackend(TestMixin, base.BACKENDS.get('deviant').__class__):
    pass


base.BACKENDS.set('gigants', GigantsTestBackend)
base.BACKENDS.set('deviant', DeviantTestBackend)


class BaseTestMixin(object):
    def __init__(self, *args, **kwargs):
        super(BaseTestMixin, self).__init__(*args, **kwargs)
        backend_name = self.__class__.__name__.lower().split('test')[0]
        self.backend = base.BACKENDS.get(backend_name)

    def setUp(self):
        if os.path.exists(self.backend.cache_filename):
            os.remove(self.backend.cache_filename)

    def test_items(self):
        for item in self.backend.get_items():
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


class GigantsTest(BaseTestMixin, unittest.TestCase):
    new_item_id = 2402


class DeviantTest(BaseTestMixin, unittest.TestCase):
    new_item_id = 359809568


class ActionsTestCase(unittest.TestCase):
    def test_to_html(self):
        backends = base.BACKENDS.all()
        output_filename = 'test_index.html'
        actions.ToHtml(backends, output_filename)

        self.assertTrue(os.path.exists(output_filename))

        with open(output_filename, 'r') as f:
            data = f.read().decode('utf-8')
            items_pairs = (list(b.get_items()) for b in backends)
            for item in reduce(list.__add__, items_pairs):
                self.assertIn(item.url, data)

        os.remove(output_filename)


if __name__ == "__main__":
    unittest.main()
