from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


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

    def check_active(self):
        if self.is_active:
            return True
        return False

    def get_uidb64(self):
        return urlsafe_base64_encode(force_bytes(self.pk)).decode()

    def get_password_reset_token(self):
        last_login = self.last_login
        password = self.password

    @classmethod
    def get_user_by_email(cls, email):
        try:
            user = cls.objects.get(email=email)
            return user
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_user_by_id(cls, id):
        try:
            user = cls.objects.get(id=id)
            return user
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_user_by_uidb64(cls, uidb64):
        user = cls.objects.get(id=urlsafe_base64_decode(force_bytes(uidb64)).decode())
        return user


class PasswordRecovery(models.Model):
    pass
