from django.test import TestCase
from django.urls import reverse
# Django by default has its user model. You can access it using this line.
from django.contrib.auth import get_user_model

from rest_framework import status

from core.models import Tag, Ingredient, Recipe

from core import models

TAGS_URL = reverse('recipe:tag-list')
INGREDIENTS_URL = reverse('recipe:ingredient-list')
RECIPES_URL = reverse('recipe:recipes')

# Samples
def sample_tag(user, name='Main course'):
    """
    Create and return a sample tag
    """

    return Tag.objects.create(user=user, name=name) 

def sample_ingredient(user, name='Cinnamon'):
    """
    Create and return a sample ingredient
    """
    
    return Ingredient.objects.create(user=user, name=name)

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

    return Recipe.objects.create(user=user, **defaults)

def sample_user(email='test@amadora.com', password='testpass'):
    """
    return a user for testing our models.
    """
    return get_user_model().objects.create_user(email,password)

def detail_url(recipe_id):
    """
    Return recipe detail URL
    """
    
    return reverse('recipe:recipe-detail', args=[recipe_id])

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
    
    def test_tag_str(self):
        """
        Test the tag's string representation
        """
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        # Take note that we hope that whatever tag is as an object when we convert it to string it should be equal to its name. Thats the effect we're lookiung for.
        self.assertEqual(str(tag), tag.name)
    
    # Tag creation
    def test_create_tag_successful(self):
        """
        Test creating a new tag
        """
        
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
    
    def test_create_tag_invalid(self):
        """
        Test creating a new tag with invalid payload
        """
        
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Ingredients test
    def test_ingredient_str(self):
        """
        Test the ingredient string respresentation
        """

        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Lemon'
        )

        self.assertEqual(str(ingredient), ingredient.name)
    
    def test_create_ingredient_successful(self):
        """
        Test create a new ingredient
        """

        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """
        Test creating ingredient fails when wrong data is supplied
        """

        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Recipe test cases
    def test_recipe_str(self):
        """
        Test the recipe string representation
        """

        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Champorado',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
    
    def test_view_recipe_detail(self):
        """
        Test viewing a recipe detail
        """

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_basic_recipe(self):
        """
        Test creating recipe
        """

        payload = {
            'title': 'Chocolate amazing cake',
            'time_minutes': 30,
            'price': 5.00
        }
        
        res = self.client.post(RECIPES_URL, payload)
        # This is new. that HTTP request should return everytime we create something new in the database
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        # This will loop at check the value of the key in the payload because its a dictionary. Getattr allows you to get a key from the object in the 1st parameter.
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """
        Test creating a recipe with tags
        """

        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')
        payload = {
            'title': 'Avocado lime cheesecake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """
        Test creating recipe with ingredients
        """
        
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')
        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price': 7.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
    
    # Updating recipes
    def test_partial_update_recipe(self):
        """
        Test updating a recipe with patch
        """

        # Adding the recipe
        recipe = sample_recipe(user=self.user)
        # Adding our sample tag to our sample recipe
        recipe.tags.add(sample_tag(user=self.user))
        # Creating a new tag to update the recipe with
        new_tag = sample_tag(user=self.user, name='Curry')
        # The payload will contain the name of the title and the Tag to be added.
        payload = {
            'title': 'Chicken tikka', 
            'tags': [new_tag.id]
        }
        # To get into the specific Recipe, I need the ID of the Recipe. I get that here
        url = detail_url(recipe.id)
        # I make the Patch request with the URL and the Payload
        self.client.patch(url, payload)
        # Refresh the db
        recipe.refresh_from_db()
        # Check the recipe. Check if title of the payload and the recipe that I updated are the same
        self.assertEqual(recipe.title, payload['title'])
        # grab all the tags from the recipe
        tags = recipe.tags.all()
        # Im updating the tag inside the recipe with the Tag i made so the recipe's tag should still be 1
        self.assertEqual(len(tags), 1)
        # Check that the new tag is inside the tags
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """
        Test updating a recipe with put
        """

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {
            'title': 'Spaghetti carbonara',
            'time_minutes': 25,
            'price': 5.00
        }
        
        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)

    # This is basically telling us that i need a uuid format of uuid version 4
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
        Test that image is saved in the correct location
        """
        # Any name will do
        uuid = 'test-uuid'
        # In order to use this line of code I have to have done @patch() from above. This forces the mockuid to become the uid specified
        mock_uuid.return_value = uuid
        # The function I plan to make. This function will return the path of the image we uploaded.
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        # I expect it to be saved in this path
        exp_path = f'uploads/recipe/{uuid}.jpg'
        # Test if its the path I wanted.
        self.assertEqual(file_path, exp_path)