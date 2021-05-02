from django.db import models
from toktok.apps.imagegallery import models as image_gallery_model
from toktok.apps.basicapp import models as basicapp_model
from django.conf import settings
from toktok.apps.storemanagerapp.models import StoreManagerBasicDetail

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(basicapp_model.Location, on_delete=models.CASCADE)
    manager = models.ForeignKey(StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)

class MenuCollection(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey(StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
        
class SubType(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey(StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
    
class Addons(models.Model):
    name = models.CharField(max_length=255)
    amountInCents = models.IntegerField()
    description = models.TextField()

class Food(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey(StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
    amountInCents = models.IntegerField(null=True)
    MenuCollection = models.ForeignKey(MenuCollection, on_delete=models.CASCADE)
    addons = models.ManyToManyField(Addons)

class FoodSubType(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    subtype = models.ForeignKey(SubType, on_delete=models.CASCADE)
    amountInCents = models.IntegerField()

class FoodCombo(models.Model):
    name = models.CharField(max_length=255)
    foods = models.ManyToManyField(Food)
    priceInCents = models.IntegerField()
    image = models.ForeignKey(image_gallery_model.Image)