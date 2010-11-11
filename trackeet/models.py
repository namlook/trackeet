
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

class Tag(Root):
    """
    A Tag is something we're working on and we'd like to track the time we
    spent on it.

    """
    __collection__ = 'tags'
    structure = {
        '_id': unicode,
    }

class Entry(Root):
    """
    An Entry is a piece of time spent on a project. It could have tags or
    comments.
    """
    __collection__ = 'entries'
    structure = {
        'project': unicode,
        'duration': int, #minutes
        'created_at': datetime,
        'comments': [unicode],
        'tags': [unicode],
    }
    required_fields = ['project', 'duration', 'created_at']

