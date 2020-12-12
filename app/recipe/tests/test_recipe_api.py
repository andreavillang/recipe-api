from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

import os.path

RECIPES_URL = reverse('recipe:recipe-list')

def sample_recipe(user, **params):
    """
    Create and return a sample recipe
    """
    
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 3,
        'price': 99.00
    }

    defaults.update(params)

    return Recipe.objects.create(user = user, **defaults)

class PublicRecipeApiTests(TestCase):
    """
    Test unauthenticated recipe API access
    """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that authentication is required
        """

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """
    Test authenticated recipe API access
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@amadora.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """
        Test retrieving a list of recipes
        """
        # Declaring it twice to create 2 recipes
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        # Standard call
        res = self.client.get(RECIPES_URL)
        # Grab all recipes and order them by ID
        recipes = Recipe.objects.all().order_by('-id')
        # Im expecting a list so thats why many=True
        serializer = RecipeSerializer(recipes, many=True)
        # Make sure that the request is valid and not turned down by the server
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check for the data
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """
        Test retrieving recipes for the specific user
        """
        # Apart from the sample user, create another one
        user2 = get_user_model().objects.create_user(
            'other@amadora.com',
            'password123'
        )
        # Make a recipe for the 2nd user
        sample_recipe(user=user2)
        # Make recipe for the 1st
        sample_recipe(user=self.user)
        # Make the call
        res = self.client.get(RECIPES_URL)
        # Grab the list of recipes from the 1st user
        recipes = Recipe.objects.filter(user=self.user)
        # Its a list like before
        serializer = RecipeSerializer(recipes, many=True)
        # Make sure that the request is good
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Im supposed to recieve only 1 recipe since i made only one
        self.assertEqual(len(res.data), 1)
        # Check if the 1 thing retrieved is the data I wanted.
        self.assertEqual(res.data, serializer.data)

class RecipeImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@amadora.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(user=self.user)
	#Teardown runs immediately after setrUp We're just making sure no lingering data
    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """
				Test uploading an image to recipe
				"""
				#Im using the recipe i just created in setup for the url
        url = image_upload_url(self.recipe.id)
				# Creating a temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
				#We check that the path exists in our LOCAL
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """
				Test uploading an invalid image
				"""
        url = image_upload_url(self.recipe.id)
				#Just a normal JSON object
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)