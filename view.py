
from flask import (Flask,
    render_template,
    request,
    g,
    redirect,
    url_for,
    flash)
from models import *
from mongokit import Connection
from datetime import datetime

# create our application
app = Flask(__name__)
app.config['DATABASE'] = 'trackeet'
app.config['SECRET_KEY'] = 'secret'
app.debug = True

# register models
con = Connection()
con.register([Project, Task, Entry])

def get_db():
    return con[app.config['DATABASE']]

@app.before_request
def before_request():
    g.db = get_db()

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
    project_id =  request.form['project']
    task_name = request.form['task']
    duration = int(request.form['duration'])
    if not g.db.Project.find_one(project_id):
        project = g.db.Project()
        project['_id'] = project_id
        project.save()
    task = g.db.Project.find_one({'name':task_name, 'project':project_id})
    if not task:
        task = g.db.Task()
        task['name'] = task_name
        task['project'] = project_id
        task.save()
    entry = g.db.Entry()
    entry['duration'] = duration
    entry['task'] = task['_id']
    #entry['comment'] = comment
    entry['created_at'] = datetime.utcnow()
    entry.save()
    flash('entry created', 'success') 
    return redirect(url_for('new_entry'))
    

if __name__ == '__main__':
    app.run()

