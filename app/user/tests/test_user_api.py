from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """
    Test the uysers API in public
    """
    
    def setUp(self):
        """
        instantiate stuff
        """
        self.client = APIClient()
        
    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        """
        payload = {
            'email': 'test@amadora.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        # res means response, we're actually using .post() to make a self post request. Given the payload we stated above
        res = self.client.post(CREATE_USER_URL, payload)
        # Now that we've made a response, lets check if its successful. We check if the respononse has a status equal to a status code that defines success.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # If success, lets check our data using the code below. This grabs the user from our db given the response
        user = get_user_model().objects.get(**res.data)
        # Now we check if the user we got back, is equal to the password we sent.
        self.assertTrue(user.check_password(payload['password']))
        # This is just to make sure that there is no password in our response because thats a security breach.
        self.assertNotIn('password', res.data)
    
    def test_password_too_short(self):
        """
        test if the password is more than 5 characters
        """
        payload = {
            'email': 'test@amadora.com',
            'password': 'pw',
            'name': 'Test name'
        }
        # same way we create a user
        res = self.client.post(CREATE_USER_URL, payload)
        # We WANT  a bad request so we're looking for that
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Now we want to check if even though it threw a bad requets, that the user was never made.
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # the exists() will return true if the modal contains the user email we used in the payload. If the user didnt get created, then its false. We check for the false.
        self.assertFalse(user_exists)