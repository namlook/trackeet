
from flask import Flask, render_template
from models import *
from mongokit import Connection

# create our application
app = Flask(__name__)
app.config['DATABASE'] = 'trackeet'
app.debug = True

# register models
con = Connection()
con.register([Project, Task, Entry])

@app.route('/entry/new')
@app.route('/')
def new_entry():
    """
    display the form page in order to create a new entry
    """
    return render_template('new_entry.html')

@app.route('/entry/create', methods=['POST'])
def create_entry():
    """
    save a entry in the database. If the task does not exists, it will create a
    new one on the fly.
    """
    pass

if __name__ == '__main__':
    app.run()

