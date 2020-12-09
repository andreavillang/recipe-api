from django.test import TestCase
# Django by default has its user model. You can access it using this line.
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        # test creating a new user with an email is successful
        email = 'test@angelo.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
		# Since we arent allowed to use password since its encrypted, we use the assertTrue function.
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        #test if email becomes normalized
        email = 'test@ANGELO.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        # test if user with no email raises an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'askjfdh')
        
    def test_create_new_superuser(self):
        # Test creating a super user
        user = get_user_model().objects.create_superuser(
            'test@angelo.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)