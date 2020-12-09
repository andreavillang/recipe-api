from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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