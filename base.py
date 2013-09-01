#!venv/bin/python
# coding: utf-8
import re
import os
import urllib2
import urlparse as u
import pickle

RE_FLAGS = re.I | re.U


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


class BackendsCache(object):
    def __init__(self):
        self._cache = {}

    def set(self, name, backend):
        self._cache[name] = backend()

    def get(self, name):
        try:
            return self._cache[name]
        except KeyError:
            return None

    def filter(self, names):
        return filter(None, map(self.get, names))

    def all(self):
        return self._cache.values()

    def all_names(self):
        return self._cache.keys()


BACKENDS = BackendsCache()


class Registered(type):
    """
    Simple metaclass for registering and validate backends.
    """
    def __init__(self, name, bases, dict):
        type.__init__(self, name, bases, dict)
        self.after_init(name, bases, dict)

    def after_init(self, name, bases, dict):
        if not self.__module__.startswith('backends.'):
            return

        attrs = ('url', 'items_urls_regexp', 'items_titles_regexp')
        for i, attr in enumerate(attrs):
            a = getattr(self, attr, None)
            if not a:
                raise AttributeError(
                    u'%s: need set %s attriute' % (name, attr))
            if i > 0:
                setattr(self, attr, re.compile(a, RE_FLAGS))

        BACKENDS.set(name.lower(), self)


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

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @cached_property
    def raw_data(self):
        r = urllib2.urlopen(self.url)  # build custom head (user-agent etc)
        return r.read().decode('utf-8')

    @property
    def cache_filename(self):
        return os.path.join('tmp', '%s.cache' % self.name)

    def save(self):
        with open(self.cache_filename, 'wb') as f:
            pickle.dump(set(x.id for x in self.get_items()), f)

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

    def get_items(self):
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
        ids = set(x.id for x in self.get_items())
        diff = ids - old_ids

        if diff:
            self.save()

        return filter(lambda x: x.id in diff, self.get_items())

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def show_notice(self):
        pass

    def callback(self):
        pass
