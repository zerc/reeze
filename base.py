#!venv/bin/python
# coding: utf-8
import re
import os
import urllib2
import urlparse as u
import pickle

RE_FLAGS = re.I | re.U
BACKENDS = {}  # backends container


## {{{ http://code.activestate.com/recipes/576563/ (r1)
def cached_property(f):
    """returns a cached property that is calculated by function f"""
    def get(self):
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x
    return property(get)
## end of http://code.activestate.com/recipes/576563/ }}}


def get_backend(name):
    try:
        return BACKENDS[name]
    except KeyError:
        return None


class Registered(type):
    """
    Simple metaclass for registering backends.
    """
    def __init__(self, name, bases, dict):
        type.__init__(self, name, bases, dict)
        if name != 'BaseBackend':
            BACKENDS[name.lower()] = self


class BaseItem(object):
    def __init__(self, url, title):
        self.url = url
        self._title = title
        self.clean_regexp = re.compile('(&nbsp;)', RE_FLAGS)

    @cached_property
    def title(self):
        return self.clean_regexp.sub('', self._title)

    @property
    def id(self):
        raise NotImplementedError(u'Implement id property for item')

    def __str__(self):
        return '<Item: %s>' % self.id


class BaseBackend(object):
    __metaclass__ = Registered

    url = None
    items_urls_regexp = None
    items_titles_regexp = None
    item_cls = BaseItem

    def __init__(self, *args, **kwargs):
        for n in 'url items_urls_regexp items_titles_regexp'.split(' '):
            if getattr(self, n) is None:
                raise NotImplementedError(u'Please set up `%s` attribute!' % n)

    @cached_property
    def raw_data(self):
        r = urllib2.urlopen(self.url)
        return r.read()

    @property
    def cache_filename(self):
        return os.path.join(
            'tmp', '%s.cache' % self.__class__.__name__.lower())

    def save(self):
        with open(self.cache_filename, 'wb') as f:
            pickle.dump(set(x.id for x in self.items), f)

    def load(self):
        try:
            with open(self.cache_filename, 'rb') as f:
                return pickle.load(f)
        except IOError:
            return False

    @cached_property
    def base_url(self):
        parsed_url = u.urlparse(self.url)
        return 'http://%s' % parsed_url.hostname

    @property
    def items(self):
        data = self.raw_data
        tmp = {}
        for x in zip(*map(lambda x: getattr(x, 'findall')(data),
                    (self.items_urls_regexp, self.items_titles_regexp))):
            item = self.item_cls(u.urljoin(self.base_url, x[0]), x[1])

            if not tmp.get(item.id):
                tmp[item.id] = True
                yield item

    @property
    def new_items(self):
        old_ids = self.load() or set([])
        ids = set(x.id for x in self.items)
        diff = ids - old_ids

        if diff:
            self.save()

        return filter(lambda x: x.id in diff, self.items)

    def show_notice(self):
        pass

    def callback(self):
        pass
