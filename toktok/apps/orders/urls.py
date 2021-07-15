from django.contrib import admin
from django.urls import path
from toktok.apps.orders.views import changeStatus, getAllOrder, getOrder, getUserOrder

urlpatterns = [
    path('getUserOrder',getUserOrder,name='getUserOrder'),
    path('getAllOrder',getAllOrder,name='getAllOrder'),
    path('getOrder',getOrder,name='getOrder'),
    path('changeStatus',changeStatus,name='changeStatus')
    ]