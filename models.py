
from mongokit import Document
from datetime import datetime
from mongokit import ObjectId

class Root(Document):
    pass

class Project(Root):
    """
    A time tracked project.
    """
    __collection__ = 'projects'
    structure = {
        '_id': unicode # name
    }

class Task(Root):
    """
    A Task is something we're working on and we'd like to track the time we
    spent on it.

    A task is assigned to a project.
    """
    __collection__ = 'tasks'
    structure = {
        'project': unicode,
        'name': unicode,
    }
    required_fields = ['project', 'name']

class Entry(Root):
    """
    An Entry is a piece of time spent on a Task.
    """
    __collection__ = 'entries'
    structure = {
        'task': ObjectId,
        'duration': int, #minutes
        'created_at': datetime,
        'comment': unicode,
    }
    required_fields = ['task', 'duration', 'created_at']

