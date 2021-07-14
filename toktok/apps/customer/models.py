from django.db import models
from toktok import settings
from toktok.apps.basicapp import models as basicapp_models
from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from toktok.apps.storemanagerapp.manager import StoreManagerUserController
from ..imagegallery.models import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(null=True, blank=True)

class Rider(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(null=True, blank=True)


class User(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('verified'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_rider=models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)