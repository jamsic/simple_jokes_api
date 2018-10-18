import base64
import unittest
from flask_app import app
from flask_app.models import UserModel, JokeModel, session


class UsersTestCase(unittest.TestCase):

    TEST_USERS_ENDPOINT = 'v1/users'
    TEST_USER_ENDPOINT = 'v1/users/{0}'
    TEST_JOKES_ENDPOINT = 'v1/users/{0}/jokes'
    TEST_JOKE_ENDPOINT = 'v1/users/{0}/jokes/{1}'
    TEST_USERNAME = 'Dino'
    TEST_PASSWORD = 'Tirex'
    NON_EXISTING_ID = 1000

    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.user = {'username': self.TEST_USERNAME,
                     'password': self.TEST_PASSWORD}
        self.empty_user = {'username': '', 'password': ''}

    def tearDown(self):
        session.query(JokeModel).delete()
        session.query(UserModel).delete()
        session.commit()

    def get_non_exisiting_id(self):
        return self.NON_EXISTING_ID

    def add_test_user_return_id(self, user=None):
        if user is None:
            user = self.user
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=user)
        return response.json['user']['id']

    def add_joke_to_user_return_id(self, user_id):
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(user_id)
        response = self.client.post(url, headers=headers)
        return response.json['joke']['id']

    def get_basic_auth_headers(self, user=None):
        if user is None:
            user = self.user
        headers = {
                   'Authorization': 'Basic ' +
                   base64.b64encode(user['username'] +
                                    ':' + user['password'])
                  }
        return headers

    # GET v1/users/{0}/jokes

    def test_get_jokes_of_existing_user_no_auth__401_unauthorized(self):
        existing_user_id = self.add_test_user_return_id()
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_jokes_of_non_existing_user_no_auth__401_unauthorized(self):
        non_existing_user_id = self.get_non_exisiting_id()
        url = self.TEST_JOKES_ENDPOINT.format(non_existing_user_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_jokes_of_existing_user_wrong_auth__401_unauthorized(self):
        other_user = {'username': 'other', 'password': 'other'}
        response1 = self.client.post(self.TEST_USERS_ENDPOINT, json=other_user)
        existing_user_id = response1.json['user']['id']
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id)
        response2 = self.client.get(url, headers=headers)
        self.assertEqual(response2.status_code, 401)

    def test_get_jokes_of_non_existing_user_wrong_auth__401(self):
        non_existing_user_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(non_existing_user_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_get_jokes_another_non_existing_user__403_forbidden(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        headers = self.get_basic_auth_headers()
        non_existing_user_id = self.get_non_exisiting_id()
        url = self.TEST_JOKES_ENDPOINT.format(non_existing_user_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_jokes_another_existing_user__403_forbidden(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        headers = self.get_basic_auth_headers()
        ouser = {'username': 'other', 'password': 'other'}
        response2 = self.client.post(self.TEST_USERS_ENDPOINT, json=ouser)
        existing_user_id = response2.json['user']['id']
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_jokes_correct_auth__200_OK(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        user_id = response.json['user']['id']
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(user_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)

    # POST v1/users/{0}/jokes

    def test_post_jokes_of_existing_user_no_auth__401_unauthorized(self):
        existing_user_id = self.add_test_user_return_id()
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 401)

    def test_post_jokes_of_non_existing_user_no_auth__401_unauthorized(self):
        non_existing_user_id = self.get_non_exisiting_id()
        url = self.TEST_JOKES_ENDPOINT.format(non_existing_user_id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_post_jokes_of_existing_user_wrong_auth__401_unauthorized(self):
        other_user = {'username': 'other', 'password': 'other'}
        response1 = self.client.post(self.TEST_USERS_ENDPOINT, json=other_user)
        existing_user_id = response1.json['user']['id']
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id)
        response2 = self.client.post(url, headers=headers)
        self.assertEqual(response2.status_code, 401)

    def test_post_jokes_of_non_existing_user_wrong_auth__401(self):
        non_existing_user_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(non_existing_user_id)
        response = self.client.post(url, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_post_jokes_another_non_existing_user__403_forbidden(self):
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=self.user)
        headers = self.get_basic_auth_headers()
        non_existing_user_id = self.get_non_exisiting_id()
        url = self.TEST_JOKES_ENDPOINT.format(non_existing_user_id)
        response = self.client.post(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_post_jokes_another_existing_user__403_forbidden(self):
        self.add_test_user_return_id()
        headers = self.get_basic_auth_headers()
        ouser = {'username': 'other', 'password': 'other'}
        response = self.client.post(self.TEST_USERS_ENDPOINT, json=ouser)
        existing_user_id = response.json['user']['id']
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id)
        response = self.client.post(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_post_jokes_correct_auth__201_created(self):
        user_id = self.add_test_user_return_id()
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKES_ENDPOINT.format(user_id)
        response = self.client.post(url, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('text', response.json['joke'])

    # GET v1/users/{0}/jokes/{1}

    def test_get_non_existing_joke_of_existing_user_no_auth__401(self):
        existing_user_id = self.add_test_user_return_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             non_existing_joke_id)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, 401)

    def test_get_non_existing_joke_of_non_existing_user_no_auth__401(self):
        non_existing_user_id = self.get_non_exisiting_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        url = self.TEST_JOKE_ENDPOINT.format(non_existing_user_id,
                                             non_existing_joke_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_existing_joke_of_existing_user_no_auth__401(self):
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_non_existing_joke_of_existing_user_wrong_auth__401(self):
        existing_user_id = self.add_test_user_return_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers(self.empty_user)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             non_existing_joke_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_get_non_exist_joke_of_non_exist_user_wrong_auth__401(self):
        non_existing_user_id = self.get_non_exisiting_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers(self.empty_user)
        url = self.TEST_JOKE_ENDPOINT.format(non_existing_user_id,
                                             non_existing_joke_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_get_existing_joke_of_existing_user_wrong_auth__401_unauth(self):
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        headers = self.get_basic_auth_headers(self.empty_user)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_get_existing_joke_of_another_user__403_forbidden(self):
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id1 = self.add_test_user_return_id(ouser)
        headers = self.get_basic_auth_headers(ouser)
        url = self.TEST_JOKES_ENDPOINT.format(existing_user_id1)
        response = self.client.post(url, headers=headers)
        existing_joke_id1 = response.json['joke']['id']
        existing_user_id2 = self.add_test_user_return_id()
        headers2 = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id1,
                                             existing_joke_id1)
        response = self.client.get(url, headers=headers2)
        self.assertEqual(response.status_code, 403)

    def test_get_non_existing_joke_of_another_user__403_forbidden(self):
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id1 = self.add_test_user_return_id(ouser)
        headers = self.get_basic_auth_headers(ouser)
        non_existing_joke_id1 = self.get_non_exisiting_id()
        existing_user_id2 = self.add_test_user_return_id()
        headers2 = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id1,
                                             non_existing_joke_id1)
        response = self.client.get(url, headers=headers2)
        self.assertEqual(response.status_code, 403)

    def test_get_non_existing_joke__404_not_found(self):
        existing_user_id = self.add_test_user_return_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             non_existing_joke_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_get_anothers_existing_joke_succ_auth__404_not_found(self):
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        headers2 = self.get_basic_auth_headers(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id2,
                                             existing_joke_id1)
        response = self.client.get(url, headers=headers2)
        self.assertEqual(response.status_code, 404)

    def test_get_existing_joke__200_ok(self):
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)

    # PUT v1/users/{0}/jokes/{1}

    def test_put_existing_joke_wrong_parameters__400_bad_request(self):
        data = {'data': 'data'}
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 400)

    def test_put_existing_joke_empty_data__400_bad_request(self):
        data = {'text': ''}
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 400)

    def test_put_existing_joke_no_auth__401_unauthorized(self):
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)

    def test_put_another_existing_joke_another_user__403_forbidden(self):
        data = {'text': 'a'}
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        headers2 = self.get_basic_auth_headers(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id1,
                                             existing_joke_id1)
        response = self.client.put(url, headers=headers2, json=data)
        self.assertEqual(response.status_code, 403)

    def test_put_my_existing_joke_to_another_user__403_forbidden(self):
        data = {'text': 'a'}
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        headers = self.get_basic_auth_headers()
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id2,
                                             existing_joke_id1)
        response = self.client.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 403)

    def test_put_non_existing_joke_succ_auth__404_not_found(self):
        data = {'text': 'a'}
        existing_user_id = self.add_test_user_return_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             non_existing_joke_id)
        response = self.client.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 404)

    def test_put_anothers_existing_joke_succ_auth__404_not_found(self):
        data = {'text': 'a'}
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        headers2 = self.get_basic_auth_headers(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id2,
                                             existing_joke_id1)
        response = self.client.put(url, headers=headers2, json=data)
        self.assertEqual(response.status_code, 404)

    def test_put_my_existing_joke_succ_auth__200_ok(self):
        data = {'text': 'a'}
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.json['joke']['text'], data['text'])

    # DELETE v1/users/{0}/jokes/{1}

    def test_delete_existing_joke_no_auth__401_unauthorized(self):
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_delete_another_existing_joke_another_user__403_forbidden(self):
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        headers2 = self.get_basic_auth_headers(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id1,
                                             existing_joke_id1)
        response = self.client.delete(url, headers=headers2)
        self.assertEqual(response.status_code, 403)

    def test_delete_my_existing_joke_to_another_user__403_forbidden(self):
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        headers = self.get_basic_auth_headers()
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id2,
                                             existing_joke_id1)
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_delete_non_existing_joke_succ_auth__404_not_found(self):
        existing_user_id = self.add_test_user_return_id()
        non_existing_joke_id = self.get_non_exisiting_id()
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             non_existing_joke_id)
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_anothers_existing_joke_succ_auth__404_not_found(self):
        existing_user_id1 = self.add_test_user_return_id()
        existing_joke_id1 = self.add_joke_to_user_return_id(existing_user_id1)
        ouser = {'username': 'other', 'password': 'other'}
        existing_user_id2 = self.add_test_user_return_id(ouser)
        headers2 = self.get_basic_auth_headers(ouser)
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id2,
                                             existing_joke_id1)
        response = self.client.delete(url, headers=headers2)
        self.assertEqual(response.status_code, 404)

    def test_delete_my_existing_joke_succ_auth__200_ok(self):
        existing_user_id = self.add_test_user_return_id()
        existing_joke_id = self.add_joke_to_user_return_id(existing_user_id)
        headers = self.get_basic_auth_headers()
        url = self.TEST_JOKE_ENDPOINT.format(existing_user_id,
                                             existing_joke_id)
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

