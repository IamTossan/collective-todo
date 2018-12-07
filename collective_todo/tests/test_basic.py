import unittest
import base64

from collective_todo import app, db
from collective_todo.seeders.superuser import create_superuser

TEST_DB = 'test'

class BasicTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/' + TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        create_superuser()

    def tearDown(self):
        pass

    def getToken(self):
        """Returns the superuser token"""

        login = self.login()
        token = login.get_json()['token']
        return token

    def login(self, name='root', password='root'):
        """Returns the response to login"""

        return self.app.get(
            '/login',
            headers={"Authorization": "Basic {}".format(base64.b64encode(b"root:root").decode("utf8"))}
        )

    def test_user_get(self):
        """It should get the list of users"""

        response = self.app.get(
            '/user',
            follow_redirects=True,
            headers={"x-access-token": self.getToken()}
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
