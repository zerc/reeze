#!venv/bin/python
# coding: utf-8
import re
import os
import unittest

import run
import base
import backends


class TestMixin(object):
    def __init__(self, *args, **kwargs):
        self.prefix = self.__class__.__name__.lower().split('test')[0]
        self.set_less_items_filename()
        base.BACKENDS.set(self.prefix, self)  # overwrite backend
        super(TestMixin, self).__init__(*args, **kwargs)

    @property
    def raw_data(self):
        with open(os.path.join('for_tests', self.tmp_filename), 'r') as r:
            return r.read()

    def set_items_filename(self):
        self.tmp_filename = '%s_items.html' % self.prefix

    def set_less_items_filename(self):
        self.tmp_filename = '%s_less_items.html' % self.prefix


## TODO: auto do it
class GigantsTestBackend(TestMixin, base.BACKENDS.get('gigants')):
    pass


class DeviantTestBackend(TestMixin, base.BACKENDS.get('deviant')):
    pass


class BaseTestMixin(object):
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
    backend = GigantsTestBackend()
    new_item_id = 2402


class DeviantTest(BaseTestMixin, unittest.TestCase):
    backend = DeviantTestBackend()
    new_item_id = 359809568


class RunTestCase(unittest.TestCase):
    def test_get_backend_name(self):
        cases = (
            (['run.py'], None),
            (['run.py', 'a'], 'a'),
            (['run.py', 'a', 'b'], 'a'),
        )
        f = run.get_backend_name

        for cond, result in cases:
            self.assertEqual(f(cond), result)

    def test_get_backends(self):
        f = run.get_backends
        self.assertEqual(len(f(None)), len(base.BACKENDS.all()))
        self.assertIsNone(f('not_realy_backend'))
        self.assertIs(f('gigants')[0], base.BACKENDS.get('gigants'))

if __name__ == "__main__":
    unittest.main()
