
from view import app
from flask import Flask
from flaskext.testing import TestCase

class MyTest(TestCase):

    def create_app(self):
        return app

    def test_hello_world(self):
        resp = self.client.get('/')
        self.assert200(resp)
        assert 'Hello World!' in resp.data

