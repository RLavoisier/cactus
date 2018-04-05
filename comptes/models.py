from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models

# Create your models here.
from comptes.model_managers import CactusUserManager

test = User

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ,
    )
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = CactusUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
