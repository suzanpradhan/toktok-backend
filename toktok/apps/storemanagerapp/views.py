from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http.response import HttpResponse
from . import forms as store_manager_forms
from django.contrib.auth import authenticate, login, logout
from toktok.apps.restaurant import models as restaurant_models
from toktok.apps.imagegallery import models as image_gallery_models
from toktok.apps.basicapp import models as basicapp_models
from toktok.apps.storemanagerapp import models as store_manager_app_models
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
        if user is not None:
            login(request, user)
            return redirect('store_manager_dashboard')
        else:
            return redirect('store_manager_login')

class FoodAllItems(TemplateView):
    template_name = "storemanagerapp/foods/all_items.html"

    def get(self, request, *args, **kwargs):
        food_items = restaurant_models.Food.objects.all()
        context = {
            "food_items": food_items
        }
        return render(request, self.template_name, context)

class FoodItemDelete(TemplateView):

    def get(self, request, id,  *args, **kwargs):
        try:
            food_item = restaurant_models.Food.objects.get(id=id, manager=request.user)
            food_item.delete()
            return redirect('store_manager_food_all_items')
        except Exception as e:
            return redirect('store_manager_food_all_items')
        

class FoodAddItemPage(LoginRequiredMixin, TemplateView):
    template_name = 'storemanagerapp/foods/add_new_item.html'
    login_url = "store_manager_login"
    redirect_field_name = "hollaback"

    def get(self, request, *args, **kwargs):
        food_menus = restaurant_models.MenuCollection.objects.filter(manager=request.user)
        # food_addons = restaurant_models.Addons.objects.all()
        # food_variations = restaurant_models.SubType.objects.all()
        context = {
            "food_menus" : food_menus,
            # "food_addons" : food_addons,
            # "food_variations": food_variations
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        food_name = request.POST.get('food_name')
        food_sku = request.POST.get('food_sku')
        food_description = request.POST.get('food_description')
        food_menu = request.POST.get('food_menu')
        food_image = request.FILES['food_image']
        food_addons = request.POST.getlist('food_addons')
        food_variations = request.POST.getlist('food_variations')
        price = int(float(request.POST.get('item_price'))*100)
        store_manager = request.user

        food = restaurant_models.Food()
        food.name = food_name
        food.sku = food_sku
        food.description = food_description
        if food_image:
            image = image_gallery_models.Image()
            image.image_name = food_image.name
            image.image = food_image
            image.save()
            food.cover_image = image
        food.manager = store_manager
        food.amountInCents = price
        if food_menu:
            menu = restaurant_models.MenuCollection.objects.get(name=food_menu)
            food.MenuCollection = menu
        food.save()
        if food_addons:
            for food_addon in food_addons:
                if food_addon:
                    variation = restaurant_models.Addons.objects.get(name=food_addon)
                    food.addons.add(variation)
        
        return redirect('store_manager_food_all_items')

class FoodAllMenus(TemplateView):
    template_name = 'storemanagerapp/foods/all_menus.html'

    def get(self, request, *args, **kwargs):
        food_menus = restaurant_models.MenuCollection.objects.all()
        # food_items_of_menus = None
        # for food_menu in food_menus:
        #     food_items = restaurant_models.Food.objects.filter(MenuCollection=food_menu.id)
        #     if len(food_items) != 0:
        #         food_items_of_menus += food_items 
        context = {
            # "menu_range": range(len(food_menus)-1),
            "food_menus": food_menus,
            # "food_items_of_menus": food_items_of_menus
        }
        return render(request, self.template_name, context)

class FoodMenuDelete(TemplateView):
    
    def get(self, request, id,  *args, **kwargs):
        try:
            food_menu = restaurant_models.MenuCollection.objects.get(id=id, manager=request.user)
            food_menu.delete()
            return redirect('store_manager_food_all_menus')
        except Exception as e:
            return redirect('store_manager_food_all_menus')


class FoodAddNewMenu(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_menu.html'

    def get(self, request, *args, **kwargs):
        food_items = restaurant_models.Food.objects.all()
        context = {
            "food_items": food_items
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        menu_name = request.POST.get("menu_name")
        food_items = request.POST.getlist("menu_name")

        menu = restaurant_models.MenuCollection(name=menu_name, manager=request.user)
        menu.save()
        print(menu)
        return redirect('store_manager_food_all_menus')

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
        addon_name = request.POST.get('addon_name')
        price = float(request.POST.get('addon_price'))
        addon = restaurant_models.Addons(name=addon_name, amountInCents=int(price*100))
        addon.save()
        print(addon)
        return redirect('store_manager_food_all_addons')

class FoodAllVariations(TemplateView):
    template_name = 'storemanagerapp/foods/all_variations.html'

    def get(self, request, *args, **kwargs):
        variations = restaurant_models.SubType.objects.filter(manager=request.user)
        context = {
            "variations": variations
        }
        return render(request, self.template_name, context)

class FoodVariationDelete(TemplateView):
    
    def get(self, request, id,  *args, **kwargs):
        try:
            variation = restaurant_models.SubType.objects.get(id=id, manager=request.user)
            variation.delete()
            return redirect('store_manager_food_all_variations')
        except Exception as e:
            return redirect('store_manager_food_all_variations')
    
class FoodAddNewVariation(TemplateView):
    template_name = 'storemanagerapp/foods/add_new_variation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        variation_name = request.POST.get('variation_name')
        price = float(request.POST.get('variation_price'))
        subType = restaurant_models.SubType(name=variation_name, manager=request.user)
        subType.save()
        return redirect('store_manager_food_all_variations')


class RestaurantAddNew(TemplateView):
    template_name = "storemanagerapp/restaurant/add_new_restaurant.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_description = request.POST.get('restaurant_description')
        restaurant_image = request.FILES['restaurant_image']
        restaurant_address = request.POST.get('restaurant_address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        restaurant = restaurant_models.Restaurant()
        restaurant.name = restaurant_name
        restaurant.description = restaurant_description
        if restaurant_image:
            image = image_gallery_models.Image()
            image.image_name = restaurant_image.name
            image.image = restaurant_image
            image.save()
            restaurant.cover_image = image
        if restaurant_address:
            location = basicapp_models.Location()
            location.name = restaurant_address
            location.latitude = latitude
            location.longitude = longitude
            location.save()
            restaurant.location = location
        restaurant.manager = request.user
        restaurant.save()
        return redirect('restaurant_all')

class RestaurantAll(TemplateView):
    template_name = "storemanagerapp/restaurant/all_restaurant.html"

    def get(self, request, *args, **kwargs):
        restaurants = restaurant_models.Restaurant.objects.filter(manager=request.user)
        context = {
            "restaurants": restaurants
        }
        return render(request, self.template_name, context)

class RestaurantDelete(TemplateView):
    
    def get(self, request, id,  *args, **kwargs):
        try:
            restaurant = restaurant_models.Restaurant.objects.get(id=id, manager=request.user)
            restaurant.delete()
            return redirect('restaurant_all')
        except Exception as e:
            return redirect('restaurant_all')

class GeneralSettings(TemplateView):
    template_name = "storemanagerapp/settings/general.html"

    def get(self, request, *args, **kwargs):
        store_manager_detail = None
        try:
            store_manager_detail = store_manager_app_models.StoreManagerBasicDetial.objects.get(manager=request.user)
            print(store_manager_detail)
            print(store_manager_detail.name)
        except Exception as e:
            store_manager_detail = None
        context = {
            "store_manager_detail": store_manager_detail
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs): 
        full_name = request.POST.get('full_name')
        description = request.POST.get('description')
        
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            store_manager_detail = store_manager_app_models.StoreManagerBasicDetial.objects.get(manager=request.user)
        except Exception as e:
            store_manager_detail = store_manager_app_models.StoreManagerBasicDetial()
        store_manager_detail.name = full_name
        store_manager_detail.description = description
        if request.FILES:
            cover_image = request.FILES['cover_image']
            favicon_icon = request.FILES['favicon_icon']
            store_manager_detail.cover_image = cover_image
            store_manager_detail.favicon = favicon_icon
        if address:
            location = basicapp_models.Location()
            location.name = address
            location.latitude = latitude
            location.longitude = longitude
            location.save()
            store_manager_detail.location = location
        store_manager_detail.save()
        return redirect("settings_general")

def logoutStoreManagerUser(request):
    logout(request)
    return redirect('store_manager_dashboard')