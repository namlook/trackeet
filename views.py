
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
from helpers import process_stub

from flask import Flask

# create our application
app = Flask(__name__)
app.config['DATABASE'] = 'trackeet'
app.config['SECRET_KEY'] = 'secret'


# register models
con = Connection()
con.register([Project, Tag, Entry])

@app.template_filter('forge_stub')
def forge_stub(entry):
    return ", ".join(entry['tags']+entry['comments'])

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

@app.route('/entry/create', methods=['post'])
def create_entry():
    """
    save a entry in the database. If the task does not exists, it will create a
    new one on the fly.
    """
    project_id =  request.form.get('project')
    if not project_id or not request.form.get('duration'):
        abort(400)
    duration = int(request.form['duration'])
    stub = request.form.get('stub', '')
    if stub:
        stub = process_stub(stub)
    else:
        stub = {'tags':[], 'comments':[]}
    if not g.db.Project.find_one(project_id):
        project = g.db.Project()
        project['_id'] = project_id
        project.save()
    for tag_id in stub['tags']:
        if not g.db.Tag.find_one(tag_id):
            tag = g.db.Tag()
            tag['_id'] = tag_id
            tag.save()
    entry = g.db.Entry()
    entry['project'] = project_id
    entry['duration'] = duration
    entry['tags'] = stub['tags']
    entry['comments'] = stub['comments']
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
        stub = request.form.get('stub', '')
        if stub:
            stub = process_stub(stub)
        else:
            stub = {'tags':[], 'comments':[]}
        for tag_id in stub['tags']:
            if not g.db.Tag.find_one(tag_id):
                tag = g.db.Tag()
                tag['_id'] = tag_id
                tag.save()
        entry['tags'] = stub['tags']
        entry['comments'] = stub['comments']
        if request.form.get('project'):
            if not g.db.Project.find_one(request.form['project']):
                project = g.db.Project()
                project['_id'] = request.form['project']
                project.save()
            entry['project'] = project['_id']
        entry.save()
        flash('entry updated', 'success')
    return redirect(url_for('new_entry'))

@app.route('/entry/list/<project>')
@app.route('/entry/list')
def list_entries(project=None):
    query = {}
    if project:
        query['project'] = project
    entries = g.db.Entry.find(query)
    return render_template('list_entries.html', entries=entries)

