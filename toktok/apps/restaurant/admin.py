from django.contrib import admin
from .models import Food, Addons, FoodSubType, MenuCollection, Restaurant, SubType, FoodCombo

admin.site.register(Food)
admin.site.register(Addons)
admin.site.register(SubType)
admin.site.register(FoodSubType)
admin.site.register(MenuCollection)
admin.site.register(Restaurant)
admin.site.register(FoodCombo)
