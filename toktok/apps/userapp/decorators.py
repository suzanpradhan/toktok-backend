from django.http import HttpResponse
from django.shortcuts import redirect



def unauthenticated_user(view_function):
    def wrapper_function(request, *args, kwargs):
        if not request.user.is_authenticated:
            return redirect('store_manager_login')
        else: 
            return view_function(request, *args, kwargs)
    return wrapper_function

def admin_only(view_func):
    def wrapper_function(request, *args, kwargs):
        group = None
        if request.user.is_staff:
            return view_func(request, *args, kwargs)
        else:
            return redirect('posts')
    return wrapper_function

def user_only(view_function):
    def wrapper_function(request, *args, kwargs):
        if request.user.is_staff:
            return redirect('myadmin:dashboard')
        else:
            return view_function(request, *args, kwargs)
    return wrapper_function