from django.db import models
from toktok import settings
from toktok.apps.restaurant.models import Food,Restaurant
from toktok.apps.basicapp.models import Location
from toktok.apps.storemanagerapp.models import StoreManagerBasicDetial


class FoodOrder(models.Model):
    quantity = models.ForeignKey(Food,on_delete=models.CASCADE,null=True)

class Order(models.Model):
    type=(
        (1,"Ordered"),
        (2,"Picked Up"),
        (3,"Delivering"),
        (4,"Delivered"),
    )
    manager = models.ForeignKey(StoreManagerBasicDetial, on_delete=models.CASCADE, null=True)
    foodOrder = models.ForeignKey(FoodOrder,on_delete=models.CASCADE,null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    totalAmount = models.IntegerField(null=True,blank=True)
    orderTime = models.DateTimeField(blank=True,null=True)
    deliveryTime = models.DateTimeField(blank=True,null=True)
    status = models.IntegerField(choices=type,default=1,max_length=200)

