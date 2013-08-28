# coding: utf-8
import os
from jinja2 import Environment, FileSystemLoader


class BaseAction(object):
    def __init__(self, backends, *args, **kwargs):
        for backend in backends:
            self.process_backend(backend)
        self.for_all(backends)

    def process_backend(self, backend):
        pass

    def for_all(self, backends):
        pass


class JustPrint(BaseAction):
    def process_backend(self, cls):
        print 'Process %s' % cls.__name__

        g = cls()
        new_items = g.new_items

        if not new_items:
            print "No new items"
            return

        for x in new_items:
            print x.url

        print ''


module_dir = os.path.dirname(__file__)
base_dir = os.path.dirname(module_dir)
output_filename = os.path.join(base_dir, 'index.html')


class ToHtml(BaseAction):
    def __init__(self, backends, output=output_filename, *args, **kwargs):
        self.env = Environment(loader=FileSystemLoader(module_dir))
        self.template = self.env.get_template('base.html')
        self.output = output
        super(ToHtml, self).__init__(backends, *args, **kwargs)

    def render(self, backends):
        return self.template.render(backends=backends)

    def for_all(self, backends):
        with open(self.output, 'w') as f:
            f.write(self.render(backends).encode('utf-8'))
