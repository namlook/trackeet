
from view import app, con
from flask import Flask
from flaskext.testing import TestCase

class MyTest(TestCase):

    def setUp(self):
        self.db = con['test']

    def tearDown(self):
        con.drop_database('test') 

    def create_app(self):
        app.config['DATABASE'] = 'test'
        return app

    def test_new_entry(self):
        response = self.client.get('/entry/new')
        self.assert200(response)
        assert 'Create new entry' in response.data

    def test_create_entry(self):
        response = self.client.post('/entry/create', 
          data={
            'duration':'10',
            'project': 'trackeet',
            'task': 'documentation'
          },
          follow_redirects=True
        )
        assert self.db.Project.find_one('trackeet')
        task = self.db.Task.find_one({'project':'trackeet', 'name':'documentation'})
        assert task
        assert self.db.Entry.find_one({'task': task['_id']})
        assert self.db.Entry.find_one({'task': task['_id']})
        self.assert200(response)
        assert 'entry created' in response.data

        

