from django.contrib import admin
from .models import Customer
from .models import User


admin.site.register(Customer)
admin.site.register(User)