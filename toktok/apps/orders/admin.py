from django.contrib import admin
from .models import Order,FoodOrder

admin.site.register(Order)
admin.site.register(FoodOrder)