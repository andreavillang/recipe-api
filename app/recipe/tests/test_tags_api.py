from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    """
    Tests that happen when the API is accessed publically.
    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required for retrieving tags
        """
        # Here, we're trying to get the tag without signing in.
        res = self.client.get(TAGS_URL)
        # We want it to fail.
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """
    Tests that happen when the API is accessed with a user.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@amadora.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
        Test that you can retrieve a list of tags 
        """
        # Making 2 tags that should be assigned to the user.
        Tag.objects.create(user=self.user, name='Meaty')
        Tag.objects.create(user=self.user, name='Diabetes Inducing')

        # The query
        res = self.client.get(TAGS_URL)

        # Assigning that the tags be sorted by its name in other words, alphabetical
        tags = Tag.objects.all().order_by('-name')
        # Now we need to serialize. Since this object has more than 1, we need to decalare many=True. If we dont do this itll get the top of the list
        serializer = TagSerializer(tags, many=True)
        # Check for a confirmed response.
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check if the serialized/processed data matches what we actually got.
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test that tags returned are for the specific user ONLY
        """
        # I need another user to have something to compare. Now I have 2 users
        user2 = get_user_model().objects.create_user(
            'other@amadora.com',
            'testpass'
        )
        # Add some tags to the 2nd user.
        Tag.objects.create(user=user2, name='Zesty')
        # Add some tags for the first user. This is just a shortcut to add. I assigned whatever was created to Tag
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        # Make a request, remember, the client assigned above is the first user.
        res = self.client.get(TAGS_URL)

        # Make sure the request was a success.
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check the length. I want to see that Im grabbing 1. Because thats how many tags I added
        self.assertEqual(len(res.data), 1)
        # The first user from the request. I assigned the created tag to be returned to tag. Hence im checking if the response.data is the same.
        self.assertEqual(res.data[0]['name'], tag.name)
