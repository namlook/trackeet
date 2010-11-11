
from mongokit import Document
from datetime import datetime

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
    __collection__ = 'task'
    structure = {
        'project': unicode,
        'name': unicode,
    }

class Entry(Root):
    """
    An Entry is a piece of time spent on a Task.
    """
    structure = {
        'task': unicode,
        'duration': int, #minutes
        'created_at': datetime,
        'comment': unicode,
    }
