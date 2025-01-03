from django.db import models
from toktok.apps.basicapp import models as basicapp_models
from django.contrib.auth.models import AbstractUser
from . import manager as store_manager
from django.conf import settings


class StoreManagerBasicDetail(models.Model):
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    favicon = models.ImageField(null=True, blank=True)
    location = models.ForeignKey(basicapp_models.Location, on_delete=models.CASCADE, null=True)
    token=models.CharField(null=True, max_length=500, blank=True)


class User(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = store_manager.StoreManagerUserController()

    def __str__(self):
        return self.email