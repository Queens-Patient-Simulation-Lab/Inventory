from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
# Resources on normal user models: https://docs.djangoproject.com/en/2.2/ref/contrib/auth/
# Resources for creating a custom user model
#   https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#a-full-example
#   https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

# Creating our own version of auth/user model since we authenticate by email, not username

class UserManager(BaseUserManager):
    # Specify mandatory fields as parameters and optional fields can fit in **extra_fields
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


# The fields (password, is_active, username) are included in AbstractBaseUser
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )
    objects = UserManager()
    name = models.CharField(max_length=100, default='fname lname')
    completedTutorial = models.BooleanField(default=False)
    receivesAlerts = models.BooleanField(default=False)  # Todo, would this be better as its own table relation?
    deleteFlag = models.BooleanField(default=False)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']
