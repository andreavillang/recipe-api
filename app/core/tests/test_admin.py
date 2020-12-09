from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    # setUp is a special function that allows you to make a user ahead of the test script. 
    # All its doing in the code is creating a user for us.
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@angelo.com',
            password = 'pass123'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@angelo.com',
            password = 'pass123',
            name = 'test user full name'
        )

    def test_users_listed(self):
        # Test that users are listed on user page
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_create_user_page(self):
        """
        Test that the create user page works
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_user_change_page(self):
        """
        test that the user edit page works
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # this string above basically generates this url: /admin/core/user/NUMBER IN ARGS
        
        res = self.client.get(url)

        # responses always have a status code. im comparing it to 200 which is a response OK
        self.assertEqual(res.status_code, 200)