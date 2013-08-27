# coding: utf-8
import os


# auto import all backends from `backends` package
package_dirname = 'backends'
for filaneme in os.listdir(package_dirname):
    if filaneme.endswith('.pyc') or \
            filaneme.startswith('__'):
        continue

    __import__('%s.%s' % (package_dirname, filaneme[:-3]))
