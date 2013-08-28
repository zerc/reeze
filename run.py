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


def get_backends(backend_name):
    if backend_name:
        backend = base.BACKENDS.get(backend_name)

        if backend is None:
            print 'Unknow backend %s' % backend_name
            return

    return [backend] if backend_name else base.BACKENDS.all()


def get_backend_name(argv):
    backend_name = argv[1:]
    backend_name = backend_name[0] if backend_name else None
    return backend_name


if __name__ == "__main__":
    backend_name = get_backend_name(sys.argv)
    backends = get_backends(backend_name)

    if backends:
        map(process, backends)
