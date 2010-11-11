
from view import app
from flask import Flask
from flaskext.testing import TestCase

class MyTest(TestCase):

    def create_app(self):
        return app

    def test_new_entry(self):
        resp = self.client.get('/entry/new')
        self.assert200(resp)
        assert 'Create new entry' in resp.data

