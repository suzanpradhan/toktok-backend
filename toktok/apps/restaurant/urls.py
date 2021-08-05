from django.contrib import admin
from django.urls import path
from .views import getAllFood
from toktok.apps.restaurant.views import getAllRestaurant, getFood, getRestaurant, searchFood, searchRestaurant, getAllCategories
urlpatterns = [
    path('getAllFood',getAllFood,name='getAllFood'),
    path('getAllRestaurant',getAllRestaurant,name='getAllRestaurant'),
    path('searchFood',searchFood,name='searchFood'),
    path('searchRestaurant',searchRestaurant,name='searchRestaurant'),
    path('getRestaurant',getRestaurant,name='getRestaurant'),
    path('getFood',getFood,name='getFood'),
    path('getAllCategories',getAllCategories,name='getAllCategories'),]