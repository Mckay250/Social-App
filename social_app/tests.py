from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from social_app.serializers import UserPostSerializer
from social_app.models import UserPost, User, Like

from social_app.serializers import UserSerializer
from unittest.mock import patch

# Create your tests here.

class AuthenticationTestCase(APITestCase):

    def setUp(self):
        user_object = {
            'name': "test user", 
            'email': "test.user@email.com", 
            'password': "password"
        }
        serializer = UserSerializer(data=user_object)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.user = serializer.validated_data
        self.client = APIClient()
        self.sign_up_url = reverse('sign_up')
        self.login_url = reverse('token_obtain_pair')
        
    @patch('social_app.views.get_client_ip')
    def test_user_creation_should_fail_when_invalid_email_passed(self, mock_get_client_ip):
        """
        The sign-up endpoint should return 400(bad request) when invalid email is passed
        """

        data = {
            'email' : 'test@.com',
            'name' : 'my test',
            'password' : 'not_a_password'
        }

        mock_get_client_ip.return_value = list([None, 0])
        response = self.client.post(self.sign_up_url, data)
        self.assertEqual(response.status_code, 400)
    
    @patch('social_app.views.get_client_ip')
    @patch('social_app.views.utils')
    @patch('social_app.views.tasks')
    def test_user_creation_should_be_successful_when_valid_email_passed(self, mock_tasks, mock_utils, mock_get_client_ip):
        """
        The sign-up endpoint should return 201(created) when valid email is passed
        """

        data = {
            'email' : 'test.test@gmail.com',
            'name' : 'my test',
            'password' : 'not_a_password'
        }

        mock_get_client_ip.return_value = list([None, 0])
        mock_utils.is_email_valid_format.return_value = True
        mock_tasks.populate_user_geo_location_data.delay.return_value = None
        response = self.client.post(self.sign_up_url, data)
        self.assertEqual(response.status_code, 201)
        mock_tasks.populate_user_geo_location_data.delay.assert_called()

    def test_login_return_token_given_valid_credentials(self):
        """
        The login endpoint should return an access token and a refresh token
        when valid credentials are passed in.
        """

        credentials = {
            'email' : 'test.user@email.com',
            'password' : 'password'
        }

        response = self.client.post(self.login_url, credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.json().keys())
        self.assertTrue('refresh' in response.json().keys())

    def test_login_does_not_return_token_given_invalid_credentials(self):
        """
        The login endpoint should return 401 status code
        when invalid credentials are passed in.
        """

        credentials = {
            'email' : 'test.user@email.com',
            'password' : 'password5'
        }

        response = self.client.post(self.login_url, credentials)
        self.assertEqual(response.status_code, 401)


class UserPostTestCase(APITestCase):

    def setUp(self):
        user_object = {
            'name': "test user", 
            'email': "test.user@email.com", 
            'password': "password"
        }
        serializer = UserSerializer(data=user_object)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.user = User.objects.get(id=1)
        
        self.initial_request = {
            'text': 'testing post creation'
        }
        post_serializer = UserPostSerializer(data=self.initial_request)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save(user=self.user)
        self.created_post = UserPost.objects.get(id=1)

        self.assertEqual(self.created_post.text, self.initial_request['text'])
        self.assertFalse(self.created_post.deleted)
        
        self.client = APIClient()
        self.login_url = reverse('token_obtain_pair')
        self.user_details_url = reverse('user_details')
        self.list_posts_url = reverse('list_posts')
        self.create_post_url = reverse('create_post')
        self.update_post_url = reverse('update_post')
        self.delete_post_url = reverse('delete_post')
        self.like_post_url = reverse('like_post')
        self.unlike_post_url = reverse('unlike_post')
        self.get_post_url = reverse('get_post', args=[1])

        self.access_token = self.client.post(
                self.login_url,
                {'email': 'test.user@email.com', 'password': 'password'}
            ).json()['access']


    def test_get_user_details_fail_when_bad_token_passed(self):
        """
        Should return 401(unauthorized) when bad access token is passed with request"""

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid.token.here')
        response = self.client.get(self.user_details_url)

        self.assertEqual(response.status_code, 401)
    
    def test_get_user_details_success_when_valid_token_passed(self):
        """
        Should return 200(successful) and response keys should contain name and email 
        when valid access token is passed with request
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.user_details_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.json().keys())
        self.assertTrue('email' in response.json().keys())


    def test_list_posts_fail_when_bad_token_passed(self):
        """
        Should return 401(unauthorized) when bad access token is passed with request
        """

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid.token.here')
        response = self.client.get(self.list_posts_url)

        self.assertEqual(response.status_code, 401)

    def test_list_posts_success_when_valid_token_passed(self):
        """
        Should return 200(successful) and a list when valid token is passed with request
        """
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.list_posts_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), list)
    
    def test_create_post_fail_when_bad_token_passed(self):
        """
        Should return 401(unauthorized) when bad access token is passed with request
        """

        request = {
            "text": "test post"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid.token.here')
        response = self.client.post(self.create_post_url, request)
        self.assertEqual(response.status_code, 401)
    
    def test_create_post_success_when_valid_request_body_passed(self):
        """
        Should return 201(created) when valid request body is passed with request
        """
        expected = {
            'message': 'Success'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.create_post_url, self.initial_request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected)

    def test_create_post_failed_when_invalid_request_body_passed(self):
        """
        Should return 400(bad request) when invalid request body is passed
        """
        request = {
            "texts": "test post"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.create_post_url, request)
        self.assertEqual(response.status_code, 400)

    def test_update_post_success_when_valid_request_body_passed(self):
        """
        Should return 200(success) when valid request body is passed
        """

        update_request = {
            'postId': 1,
            'text': 'updated post'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.put(self.update_post_url, update_request)
        updated_post = UserPost.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(updated_post.text, self.created_post.text)
        self.assertEqual(updated_post.text, update_request['text'])

    def test_update_post_fail_when_invalid_request_body_passed(self):
        """
        Should return 400(bad request) when invalid request body is passed
        """

        update_request = {
            'postingId': 1,
            'text': 'updated post'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.put(self.update_post_url, update_request)
        self.assertEqual(response.status_code, 400)
        
    def test_delete_post_success_when_valid_request_body_passed(self):
        """
        Should return 200(success) when valid request body is passed 
        and deleted field should be set to true
        """
        delete_request = {
            'postId': 1,
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete(self.delete_post_url, delete_request)
        updated_post = UserPost.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(updated_post.deleted)

    def test_like_post_when_valid_request_body_passed(self):
        """
        Should return 201(created) when valid request body is passed
        """
        like_request = {
            "postId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.like_post_url, like_request)
        created_like = Like.objects.get(id=1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_like.user, self.user)

    def test_unlike_post_when_non_existing_like_object(self):
        """
        Should return 404(not found) when like object is non existing
        """
        unlike_request = {
            "postId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.unlike_post_url, unlike_request)
        self.assertEqual(response.status_code, 404)

    
    def test_unlike_post_when_existing_like_object(self):
        """
        Should return 404(not found) when like object is non existing
        """
        unlike_request = {
            "postId": 1
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        like_response = self.client.post(self.like_post_url, unlike_request)
        self.assertEqual(like_response.status_code, 201)
        created_like = Like.objects.get(id=1)
        self.assertFalse(created_like.deleted)
        unlike_response = self.client.post(self.unlike_post_url, unlike_request)
        self.assertEqual(unlike_response.status_code, 200)
        deleted_like = Like.objects.get(id=1)
        self.assertTrue(deleted_like.deleted)
