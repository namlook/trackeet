
from mongokit import Connection, Document
from datetime import datetime

con = Connection()

DATABASE = 'trackeet'

class Root(Document):
    __database__ = DATABASE

@con.register
class Project(Root):
    """
    A time tracked project.
    """
    __collection__ = 'projects'
    structure = {
        '_id': unicode # name
    }

@con.register
class Task(Root):
    """
    A Task is something we're working on and we'd like to track the time we
    spent on it.

    A task is assigned to a project.
    """
    __collection__ = 'task'
    structure = {
        'project': unicode,
        'name': unicode,
    }

@con.register
class Entry(Root):
    """
    An Entry is a piece of time spent on a Task.
    """
    structure = {
        'task': unicode,
        'duration': int, #minutes
        'created_at': datetime
        'comment': unicode,
    }
