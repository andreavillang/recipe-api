import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
PermissionsMixin
from django.conf import settings

# Create your models here.
def recipe_image_file_path(instance, filename):
    """
    Generate file path for new recipe image
    """
    # Im separting the filename with its extension through this notation
    ext = filename.split('.')[-1]
    # Im getting the extension and asking the uuid function to generate 
    # me a uuid4
    filename = f'{uuid.uuid4()}.{ext}'
    # Im using the os that I imported to join the file name with the 
    # path thats acceptable to the system
    return os.path.join('uploads/recipe/', filename)

class UserManager(BaseUserManager):
		#The **extra_fields is a special datatype and it allows us to go past the parameters and still have a reference for them
    def create_user(self, email, password=None, **extra_fields):
        #Create and saves a user
        if not email:
            raise ValueError('Users must have email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
		#You cant add a password like email. instead you have to use the function in order to set a password
        user.set_password(password)
		#This allows us to save. using=self._db is just to make sure we avoid some errors.
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        # creates a superuser
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

#In the Django resources, this is already taught. Im just declaring a user under my specifications
class User(AbstractBaseUser, PermissionsMixin):
    # custom user model that supports creation with email instead of username.
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Tag(models.Model):
    """
    Tag to be used in a Recipe, "A recipe has tags that the user can add"
    """
    # We state that a Tag name can be around 255 chars in length
    name = models.CharField(max_length=255)
    # In db talk, We're assigning a foreign key which can be used to link this Tag table to another table.
    user = models.ForeignKey(
        # We want to tie this tag to the user. This is just a best practice that we grab the settings from the helper Django provides. Rather than call user above.
        settings.AUTH_USER_MODEL,
        # This setting makes sure thatwhen the user is deleted. The tag related to the user is also deleted.
        on_delete=models.CASCADE,
    )
    # This function is overriding the string representation of the tag. 
    # Instead of converting to string, we just want it to send the name.
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """
    Ingredient to be used in a recipe
    """
    
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    # Im not calling the function, rather im passing the name of the function and by rules of python im returning its address.
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title