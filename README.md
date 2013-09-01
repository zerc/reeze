Reeze
=====================

If site no have RSS but you whant whatch releases of new series fav serial (as example) - reeze help (may be :). Just specify backend for you site, add cronjob and you be fine.

### Install
Simple:

    git clone git@github.com:zerc/reeze.git reeze
    cd reeze
    virtualenv venv
    . venv/bin/activate
    pip install -r req.txt
    

Specify backend for you site (see included examples) in `backends.py`.

Run `reeze` with default options (using all backends and print new items to stdout):

    python run.py

List of available options:

    python run.py -h

Run tests:
    
    python tests.py

### This is first pre-pre-pre-alpha version. Use it in own risk. Issues are welcome ofc.
