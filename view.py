
from flask import Flask
from models import *
from mongokit import Connection

# create our application
app = Flask(__name__)
app.config['DATABASE'] = 'trackeet'
app.debug = True

# register models
con = Connection()
con.register([Project, Task, Entry])

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run()

