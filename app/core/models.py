from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from app import settings

# Create your models here.
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
    # This function is overriding the string representation of the tag. Instead of converting to string, we just want it to send the name.
    def __str__(self):
        return self.name