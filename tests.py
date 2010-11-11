
from views import app, con
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

    #
    #  Helpers
    #

    def create_entry(self, fill=False, **kwargs):
        data = {'duration':None, 'project':None, 'tag':None}
        if fill:
            data = {
                'duration':'10',
                'project': 'trackeet',
                'tag': 'documentation'
              }
        data.update(kwargs)
        return self.client.post('/entry/create',
          data=data,
          follow_redirects=True
        )

    def update_entry(self, entry, **kwargs):
        return self.client.post(
          '/entry/update/%s' % entry['_id'],
          data = kwargs,
          follow_redirects = True
        )


    #
    # Test cases
    #

    def test_new_entry(self):
        response = self.client.get('/entry/new')
        self.assert200(response)
        assert 'Create new entry' in response.data

    def test_create_entry(self):
        response = self.create_entry(fill=True)
        assert self.db.Project.find_one('trackeet')
        assert self.db.Tag.find_one('documentation')
        assert self.db.Entry.find_one({'project': 'trackeet', 'tags': 'documentation'})
        self.assert200(response)
        assert 'entry created' in response.data

    def test_create_entry_with_no_project(self):
        response = self.create_entry(duration=3)
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_update_entry(self):
        self.create_entry(fill=True)
        entry = self.db.Entry.find_one()
        response = self.update_entry(entry, duration="15")
        self.assert200(response)
        assert 'entry updated' in response.data
        new_entry = self.db.Entry.find_one()
        self.assertEqual(new_entry['duration'], 15)
        self.assertNotEqual(new_entry['duration'], entry['duration'])

    def test_update_entry_new_project(self):
        assert self.db.Project.find_one('test') is None
        self.create_entry(fill=True)
        entry = self.db.Entry.find_one()
        response = self.update_entry(entry, project="test")
        assert self.db.Project.find_one('test')

    def test_update_entry_new_tags(self):
        assert self.db.Tag.find_one('test') is None
        self.create_entry(fill=True)
        entry = self.db.Entry.find_one()
        response = self.update_entry(entry, tags="test")
        assert self.db.Tag.find_one('test')

    def test_list_all_entries(self):
        self.assert200(self.create_entry(project='trackeet_project', duration=10, tag='documentation'))
        self.assert200(self.create_entry(project='abcde_project', duration=50))
        self.assert200(self.create_entry(project='trackeet_project', duration=20, tag='tests'))
        response = self.client.get('/entry/list')
        self.assert200(response)
        assert 'trackeet_project' in response.data
        assert 'documentation' in response.data
        assert 'tests' in response.data, response.data
        assert 'abcde_project' in response.data, response.data

        response = self.client.get('/entry/list/trackeet_project')
        self.assert200(response)
        assert 'trackeet_project' in response.data
        assert 'documentation' in response.data
        assert 'tests' in response.data
        assert 'abcde_project' not in response.data, response.data

    def test_ajax_project_list(self):
        self.assert200(self.create_entry(project='trackeet_project', duration=10, tag='documentation'))
        response = self.client.get('/ajax/project/list?term=trackeet')
        self.assert200(response)
        assert 'project' in response.data
        response = self.client.get('/ajax/project/list?term=project')
        self.assert200(response)
        assert 'trackeet' in response.data

