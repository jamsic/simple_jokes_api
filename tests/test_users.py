import base64
import unittest
from flask_app import app
from flask_app.models import UserModel, JokeModel, session


class UsersTestCase(unittest.TestCase):

    TEST_USERS_ENDPOINT = 'v1/users'
    TEST_USER_ENDPOINT = 'v1/users/{0}'
    TEST_USERNAME = 'EXO-L'
    TEST_PASSWORD = 'faithful'

    def get_basic_auth_headers(self):
        headers = {
                   'Authorization': 'Basic ' +
                   base64.b64encode(self.TEST_USERNAME +
                                    ':' + self.TEST_PASSWORD)
                }
        return headers

    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.user = {'username': self.TEST_USERNAME,
                     'password': self.TEST_PASSWORD}

    def tearDown(self):
        session.query(JokeModel).delete()
        session.query(UserModel).delete()
        session.commit()

    def test_get_users__405_not_allowed(self):
        response = self.client.get(self.TEST_USERS_ENDPOINT)
        self.assertEqual(response.status_code, 405)

    def test_post_users_twice__409_user_already_exists(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        self.assertEqual(response.status_code, 409)

    def test_post_users_no_username__400(self):
        no_username_user = {'password': self.TEST_PASSWORD}
        response = self.client.post(self.TEST_USERS_ENDPOINT,
                                    json=no_username_user)
        self.assertEqual(response.status_code, 400)

    def test_post_users_no_password__400(self):
        no_password_user = {'username': self.TEST_USERNAME}
        response = self.client.post(self.TEST_USERS_ENDPOINT,
                                    json=no_password_user)
        self.assertEqual(response.status_code, 400)

    def test_post_users_no_data__400(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT)
        self.assertEqual(response.status_code, 400)

    def test_post_users_correct_data__201_created(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['user']['username'],
                         self.user['username'])

    def test_get_user_no_auth_data__401_unauthorized(self):
        user_id = 1
        url = self.TEST_USER_ENDPOINT.format(user_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_another_existing_user__403_forbidden(self):
        self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        other_user = {'username': 'other', 'password': 'other'}
        response2 = self.client.post(self.TEST_USERS_ENDPOINT,
                                     json=other_user)
        existing_user_id = response2.json['user']['id']
        url = self.TEST_USER_ENDPOINT.format(existing_user_id)
        headers = self.get_basic_auth_headers()
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_another_non_existing_user__403_forbidden(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        non_existing_user_id = 1000
        url = self.TEST_USER_ENDPOINT.format(non_existing_user_id)
        headers = self.get_basic_auth_headers()
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_user_correct_auth_data__200_OK_correct_user_got(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        new_user_id = response.json['user']['id']
        url = self.TEST_USER_ENDPOINT.format(new_user_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        headers = self.get_basic_auth_headers()
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user']['username'], self.TEST_USERNAME)

if __name__ == '__main__':
    unittest.main()

