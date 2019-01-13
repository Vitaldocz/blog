from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('You must enter a email.')
        if not password:
            raise ValueError('You must set a login password.')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(blank=True, unique=False, max_length=1)
    email = models.EmailField(blank=False, unique=True)
    verification_code = models.TextField(default=0, blank=False)
    is_active = models.BooleanField(default=False)
    mobile = models.BigIntegerField(default=None)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.get_full_name() + ' ' + self.email


class PasswordRecovery(models.Model):
    pass
