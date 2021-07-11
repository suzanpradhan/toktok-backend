from django.contrib import admin
from django.urls import path
from toktok.apps.orders.views import getAllOrder, getUserOrder,getOrder

urlpatterns = [
    path('getUserOrder',getUserOrder,name='getUserOrder'),
    path('getAllOrder',getAllOrder,name='getAllOrder'),
    path('getOrder',getOrder,name='getOrder')
    ]