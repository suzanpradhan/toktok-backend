from django.db import models
from toktok import settings
from toktok.apps.restaurant import models as restaurant_models
from toktok.apps.basicapp import models as basicapp_models
from toktok.apps.storemanagerapp import models as store_manager_app_models


class FoodOrder(models.Model):
    quantity = models.ForeignKey(restaurant_models.Food,on_delete=models.CASCADE,null=True)

class Order(models.Model):
    type=(
        (1,"Ordered"),
        (2,"Picked Up"),
        (3,"Delivering"),
        (4,"Delivered"),
    )
    manager = models.ForeignKey(store_manager_app_models.StoreManagerBasicDetail, on_delete=models.CASCADE, null=True)
    foodOrder = models.ForeignKey(FoodOrder,on_delete=models.CASCADE,null=True)
    restaurant = models.ForeignKey(restaurant_models.Restaurant,on_delete=models.CASCADE,null=True)
    location = models.ForeignKey(basicapp_models.Location,on_delete=models.CASCADE,null=True)
    totalAmount = models.IntegerField(null=True,blank=True)
    orderTime = models.DateTimeField(blank=True,null=True)
    deliveryTime = models.DateTimeField(blank=True,null=True)
    status = models.IntegerField(choices=type,default=1)

