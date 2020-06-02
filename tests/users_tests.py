import unittest
import requests
import json
from manager import create_app
from db import db


class TestUserRegister(unittest.TestCase):
    def setUp(self):
        # self.app = create_app("testing")
        # self.client = self.app.app.test_client()
        self.app = create_app("testing")
        self.client = self.app.test_client

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_register(self):

        headers = {"content-type": "application/json"}
        data = {
            "username": "Abel Orihuelass",
            "email": "abel+500@commonsense.io",
            "password": "1234",
        }
        response = self.client().post(
            "/api/v1/register", data=json.dumps(data), headers=headers
        )

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
