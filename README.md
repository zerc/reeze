Reeze
=====================

If site no have RSS but you whant whatch releases of new series fav serial (as example) - reeze help (may be :). Just specify backend for you site, add cronjob and you be fine.

### Install
Simple:

    git clone git@github.com:zerc/reeze.git reeze
    cd reeze
    

Specify backend for you site (see included examples) in `backends.py`.

Run in `reeze` folder:

    python run.py [backend_name]

Run tests:
    
    python tests.py

### This is first pre-pre-pre-alpha version. Use it in own risk. Issues are welcome ofc.

### TODO
* Fetch data from all backends
* Add some notifier functions (to email, ubuntu popup etc)
* Callback functions (who know what do with new items)
* Add auth support
