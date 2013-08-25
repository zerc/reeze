# coding: utf-8
import sys
import base
import backends

DEFAULT_BACKEND = 'gigants'


def main(backend_name):
    try:
        cls = base.BACKENDS[backend_name]
    except KeyError:
        print "Unknow backend: %s" % backend_name
        return

    g = cls()
    new_items = g.new_items

    if not new_items:
        print "No new items"
    else:
        for x in new_items:
            print x.url


if __name__ == "__main__":
    cls_name = sys.argv[1:]
    cls_name = cls_name[0] if cls_name else DEFAULT_BACKEND
    main(cls_name)
