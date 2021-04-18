from django.db import models
from toktok.apps.imagegallery import models as image_gallery_model
from toktok.apps.basicapp import models as basicapp_model

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE)
    location = models.ForeignKey(basicapp_model.Location, on_delete=models.CASCADE)

class MenuCollection(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class FoodSubType(models.Model):
    name = models.CharField(max_length=255)
    
class Addons(models.Model):
    name = models.CharField(max_length=255)
    amountInCents = models.IntegerField()  
    description = models.TextField()

class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ForeignKey(image_gallery_model.Image, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    amountInCents = models.IntegerField()
    MenuCollection = models.ForeignKey(MenuCollection, on_delete=models.CASCADE)
    FoodSubType = models.ManyToManyField(FoodSubType)

