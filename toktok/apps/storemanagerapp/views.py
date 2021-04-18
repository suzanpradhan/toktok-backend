from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from . import forms as store_manager_forms
from django.contrib.auth import authenticate, login, logout

class Dashboard(TemplateView):
    template_name = "storemanagerapp/dashboard.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class StoreMangerLogin(TemplateView):
    template_name = "storemanagerapp/auth/login.html"
    form = store_manager_forms.CustomUserCreationForm
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password1")
        user = authenticate(request, email=email, password=password)
        if user:
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")

class FoodAllItems(TemplateView):
    template_name = "storemanagerapp/foods/all_items.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FoodAddItemPage(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_item.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FoodAllMenus(TemplateView):
    template_name = 'storemanagerapp/foods/all_menus.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FoodAddNewMenu(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_menu.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FoodAddNewAddon(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_addon.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class FoodAddNewVariation(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_variation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)