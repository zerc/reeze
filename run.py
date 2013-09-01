#!venv/bin/python
# coding: utf-8
import sys
import argparse

import base
import backends
import actions


def main(args=None):
    parser = argparse.ArgumentParser(description=u"web watcher")

    choices = ['all']
    choices.extend(base.BACKENDS.all_names())
    parser.add_argument(
        'selected_backends', nargs='*', default='all',
        help=u'backends using for', choices=choices)

    parser.add_argument(
        '--output_method', default='JustPrint',
        choices=actions.actions.__ALL__,
        help=u'specify output method')

    args = parser.parse_args(args)

    if args.selected_backends == 'all':
        backends = base.BACKENDS.all()
    else:
        backends = base.BACKENDS.filter(args.selected_backends)

    getattr(actions, args.output_method)(backends)


if __name__ == "__main__":
    main()
