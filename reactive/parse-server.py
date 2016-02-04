import re
import shutil

from charmhelpers.core.hookenv import status_set
from charmhelpers.core.templating import render
from charms.reactive import when, when_not
from charms.reactive import set_state, remove_state

from nodejs import npm, node_dist_dir


@when('nodejs.available', 'mongodb.available')
def setup_parse_server(mongodb):
    print(mongodb)
    shutil.copy('index.js', 'index.js.orig')
    with open('index.js.orig') as src:
        with open('index.js', 'w') as dst:
            for line in src:
                line = str.replace('mongodb://localhost:27017/dev',
                                   'mongodb://' + mongodb + '/parse')
                dst.write(line)

    npm('install')
    npm('start')


@when_not('mongodb.available')
def nomongo_stat():
    status_set("blocked", "a mongodb relation is required")
