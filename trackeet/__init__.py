
from flask import Flask, g
from models import *
from mongokit import Connection
import os, sys

DATABASE = 'trackeet'
SECRET_KEY = 'secret'
APP_NAME = 'trackeet'

# register models
con = Connection()
con.register([Project, Tag, Entry])

from trackeet.views.entry import entry

app = Flask(__name__)
app.config.from_object(__name__)
app.register_module(entry)

@app.template_filter('forge_stub')
def forge_stub(entry):
    return ", ".join(i for i in entry['tags']+entry['comments'] if i is not None)

def get_db():
    return con[app.config['DATABASE']]

@app.before_request
def before_request():
    g.db = get_db()


