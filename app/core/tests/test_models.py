from django.test import TestCase
from django.urls import reverse
# Django by default has its user model. You can access it using this line.
from django.contrib.auth import get_user_model

from rest_framework import status

from .models import Tag, Ingredient

TAGS_URL = reverse('recipe:tag-list')
INGREDIENTS_URL = reverse('recipe:ingredient-list')

def sample_user(email='test@amadora.com', password='testpass'):
    """
    return a user for testing our models.
    """
    return get_user_model().objects.create_user(email,password)

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
    
    # TAGS
    
    def test_tag_str(self):
        """
        Test the tag's string representation
        """
        tag = Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )
        # Take note that we hope that whatever tag is as an object when 
        # we convert it to string it should be equal to its name. Thats the effect we're lookiung for.
        self.assertEqual(str(tag), tag.name)
    
    def test_create_tag_successful(self):
        """
        Test creating a new tag
        """
        
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user = self.user,
            name = payload['name']
        ).exists()
        self.assertTrue(exists)
    
    def test_create_tag_invalid(self):
        """
        Test creating a new tag with invalid payload
        """
        
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # INGREDIENTS
    
    def test_ingredient_str(self):
        """
        Test the ingredient string respresentation
        """

        ingredient = Ingredient.objects.create(
            user = sample_user(),
            name = 'Lemon'
        )

        self.assertEqual(str(ingredient), ingredient.name)
    
    def test_create_ingredient_successful(self):
        """
        Test create a new ingredient
        """

        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user = self.user,
            name = payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """
        Test creating ingredient fails when wrong data is supplied
        """

        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)