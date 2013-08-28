#!venv/bin/python
# coding: utf-8
import sys
import base
import backends
import actions


def get_backend_name(argv):
    backend_name = argv[1:]
    backend_name = backend_name[0] if backend_name else None
    return backend_name


def get_backends(backend_name):
    if backend_name:
        backend = base.BACKENDS.get(backend_name)

        if backend is None:
            print 'Unknow backend %s' % backend_name
            return

    return [backend] if backend_name else base.BACKENDS.all()


if __name__ == "__main__":
    backend_name = get_backend_name(sys.argv)
    backends = get_backends(backend_name)
    # TODO: add choice for action
    actions.JustPrint(backends)
    # actions.ToHtml([b() for b in backends])
