from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from . import forms as store_manager_forms
from django.contrib.auth import authenticate, login, logout
from toktok.apps.restaurant import models as restaurant_models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class Dashboard(LoginRequiredMixin, TemplateView):
    # login_url = 'store_manager_login'
    # redirect_field_name = 'redirect_to'
    template_name = "storemanagerapp/dashboard.html"
    login_url = "store_manager_login"
    redirect_field_name = "hollaback"
    # raise_exception = True
    # @method_decorator(login_required(login_url='store_manager_login'))
    # def dispatch(self, *args, **kwargs):
    #     return super(ProtectedView, self).dispatch(*args, **kwargs)
    # @method_decorator(unauthenticated_user)
    # def dispatch(self, *args, **kwargs):
    #     return super(Dashboard, self).dispatch(*args, **kwargs)
    # @login_required(login_url="store_manager_login")
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



class StoreMangerLogin(TemplateView):
    template_name = "storemanagerapp/auth/login.html"
    form = store_manager_forms.CustomUserCreationForm
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        login(request, user)
        print(request.user)
        if user is not None:
            return redirect('store_manager_dashboard')
        else:
            return HttpResponse("Failed")

class FoodAllItems(TemplateView):
    template_name = "storemanagerapp/foods/all_items.html"

    def get(self, request, *args, **kwargs):
        food_items = restaurant_models.Food.objects.all()
        context = {
            "food_items": food_items
        }
        return render(request, self.template_name, context)

class FoodAddItemPage(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_item.html'

    def get(self, request, *args, **kwargs):
        food_menus = restaurant_models.MenuCollection.objects.all()
        food_addons = restaurant_models.Addons.objects.all()
        food_variations = restaurant_models.SubType.objects.all()
        context = {
            "fodd_menus" : food_menus,
            "food_addons" : food_addons,
            "food_variations": food_variations
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        return HttpResponse(request.POST.get("food_addons"))

class FoodAllMenus(TemplateView):
    template_name = 'storemanagerapp/foods/all_menus.html'

    def get(self, request, *args, **kwargs):
        food_menus = restaurant_models.MenuCollection.objects.all()
        food_items_of_menus = [restaurant_models.Food.objects.get(id=food_menu.id) for food_menu in food_menus]
        context = {
            "test":range(len([1,2,3])),
            "testlen":3,
            "food_menus": food_menus,
            "food_items_of_menus": food_items_of_menus
        }
        return render(request, self.template_name, context)

class FoodAddNewMenu(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_menu.html'

    def get(self, request, *args, **kwargs):
        food_items = restaurant_models.Food.objects.all()
        context = {
            "food_items": food_items
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return HttpResponse(request.POST.get("food_items"))

class FoodAllAddons(TemplateView):
    template_name = 'storemanagerapp/foods/all_addons.html'

    def get(self, request, *args, **kwargs):
        food_addons = restaurant_models.Addons.objects.all()
        context = {
            "food_addons": food_addons
        }
        return render(request, self.template_name, context)

class FoodAddNewAddon(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_addon.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return HttpResponse(request.POST)

class FoodAllVariations(TemplateView):
    template_name = 'storemanagerapp/foods/all_variations.html'

    def get(self, request, *args, **kwargs):
        variations = restaurant_models.SubType.objects.all()
        context = {
            "variations": variations
        }
        return render(request, self.template_name, context)

class FoodAddNewVariation(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_variation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RestaurantAddNew(TemplateView):
    template_name = "storemanagerapp/restaurant/add_new_restaurant.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RestaurantAll(TemplateView):
    template_name = "storemanagerapp/restaurant/all_restaurant.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

def logoutStoreManagerUser(request):
    logout(request)
    return redirect('store_manager_dashboard')