# coding: utf-8
import sys
import base
import backends


def process(cls):
    print 'Process %s' % cls.__name__

    g = cls()
    new_items = g.new_items

    if not new_items:
        print "No new items"
        return

    for x in new_items:
        print x.url

    print ''


def main(backend_name):
    if backend_name:
        backend = base.BACKENDS.get(backend_name)

        if backend is None:
            print 'Unknow backend %s' % backend_name
            return

    backends = [backend] if backend_name else base.BACKENDS.all()
    map(process, backends)


if __name__ == "__main__":
    cls_name = sys.argv[1:]
    cls_name = cls_name[0] if cls_name else None
    main(cls_name)
