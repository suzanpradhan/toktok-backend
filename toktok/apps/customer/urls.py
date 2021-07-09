from django.contrib import admin
from django.urls import path
from .views import userRegister,userLogin,verifyToken

urlpatterns = [
    path('register',userRegister,name='register'),
    path('login',userLogin,name='login'),
    path('verify-token',verifyToken,name='verify-token')
]
