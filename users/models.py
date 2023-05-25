from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from user_choices import InterestingChoices
from users.manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    adress = models.CharField(max_length=255, null=True)
    interesting = models.CharField(choices=InterestingChoices, default='persional')
    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # put email for registration
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.get_full_name()


class SocialAccount(models.Model):
    class ProviderTypes(models.TextChoices):
        GOOGLE = "google"
        FACEBOOK = 'facebook'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_account')
    social_account = models.CharField(max_length=50, choices=ProviderTypes.choices)


class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="varifaction_codes", null=True,
                             blank=True)
    email = models.EmailField(unique=True, null=True)
    # verification_type = models.CharField(max_length=50, choices=VerificationTypes.choices)
    last_sent_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField()
    expired_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.user)

    @property
    def is_exprice(self):
        return self.expired_at < self.last_sent_time + timedelta(seconds=30)
