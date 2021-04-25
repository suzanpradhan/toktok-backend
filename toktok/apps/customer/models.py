from django.db import models
from toktok import settings
from toktok.apps.basicapp import models as basicapp_models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(null=True, blank=True)

class Rider(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(null=True, blank=True)
