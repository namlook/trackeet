
from flask import (Flask,
    render_template,
    request,
    g,
    abort,
    redirect,
    url_for,
    flash)
from models import *
from mongokit import Connection, ObjectId
from datetime import datetime

from flask import Flask

# create our application
app = Flask(__name__)
app.config['DATABASE'] = 'trackeet'
app.config['SECRET_KEY'] = 'secret'


# register models
con = Connection()
con.register([Project, Tag, Entry])

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
    tag_id = request.form['tag']
    duration = int(request.form['duration'])
    if not g.db.Project.find_one(project_id):
        project = g.db.Project()
        project['_id'] = project_id
        project.save()
    if not g.db.Tag.find_one(tag_id):
        tag = g.db.Tag()
        tag['_id'] = tag_id
        tag.save()
    entry = g.db.Entry()
    entry['project'] = project_id
    entry['duration'] = duration
    entry['tags'] = [tag_id]
    #entry['comment'] = comment
    entry['created_at'] = datetime.utcnow()
    entry.save()
    flash('entry created', 'success') 
    return redirect(url_for('new_entry'))
    
@app.route('/entry/edit/<id>', methods=['POST'])
def edit_entry(id):
    entry = g.db.Entry.find_one(ObjectId(id))
    if not entry:
        flash('entry not found', 'error')
        return redirect(url_for('new_entry'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/entry/update/<id>', methods=['POST'])
def update_entry(id):
    entry = g.db.Entry.find_one(ObjectId(id))
    if not entry:
        flash('entry not found', 'error')
    else:
        if request.form.get('duration'):
            entry['duration'] = int(request.form['duration'])
        if request.form.get('tags'):
            if not g.db.Tag.find_one(request.form.get('tags')):
                tag = g.db.Tag()
                tag['_id'] = request.form.get('tags')
                tag.save()
            entry['tags'] = [tag['_id']]
        if request.form.get('project'):
            if not g.db.Project.find_one(request.form['project']):
                project = g.db.Project()
                project['_id'] = request.form['project']
                project.save()
            entry['project'] = project['_id']
        entry.save()
        flash('entry updated', 'success')
    return redirect(url_for('new_entry'))

