from django.db import models
from toktok.apps.imagegallery import models as image_gallery_model
from toktok.apps.basicapp import models as basicapp_model
from django.conf import settings
from toktok.apps.storemanagerapp import models as store_manager_app_models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(basicapp_model.Location, on_delete=models.CASCADE)
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)

class MenuCollection(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
        
class SubType(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
    
class Addons(models.Model):
    name = models.CharField(max_length=255)
    amountInCents = models.FloatField()
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)

class FoodSubType(models.Model):
    subtype = models.ForeignKey(SubType, on_delete=models.CASCADE)
    amountInCents = models.FloatField()

class Food(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
    amountInCents = models.FloatField(null=True)
    MenuCollection = models.ForeignKey(MenuCollection, on_delete=models.CASCADE, null=True)
    subtypes = models.ManyToManyField(FoodSubType, blank=True, null=True)
    addons = models.ManyToManyField(Addons)

class FoodCombo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE, blank=True, null=True)
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
    foods = models.ManyToManyField(Food)
    addons = models.ManyToManyField(Addons)
    amountInCents = models.FloatField(null=True)

