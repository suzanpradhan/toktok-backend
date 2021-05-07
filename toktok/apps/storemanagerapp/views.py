from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http.response import HttpResponse, JsonResponse
from . import forms as store_manager_forms
from django.contrib.auth import authenticate, login, logout
from toktok.apps.restaurant import models as restaurant_models
from toktok.apps.imagegallery import models as image_gallery_models
from toktok.apps.basicapp import models as basicapp_models
from . import models as store_manager_app_models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import IsStoreManagerMixin


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "storemanagerapp/dashboard.html"
    login_url = "store_manager_login"
    redirect_field_name = "hollaback"
    def get(self, request, *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        food_items = restaurant_models.Food.objects.filter(manager=manager_model)
        restaurants = restaurant_models.Restaurant.objects.filter(manager=manager_model)
        context = {
            "food_items": food_items,
            "restaurants": restaurants
        }
        return render(request, self.template_name, context)



class StoreMangerLogin(TemplateView):
    template_name = "storemanagerapp/auth/login.html"
    form = store_manager_forms.CustomUserCreationForm
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        print(user)
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
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            food_item = restaurant_models.Food.objects.get(id=id, manager=manager_model)
            food_item.delete()
            return redirect('store_manager_food_all_items')
        except Exception as e:
            return redirect('store_manager_food_all_items')
        

class FoodAddItemPage(LoginRequiredMixin,IsStoreManagerMixin, TemplateView):
    template_name = 'storemanagerapp/foods/add_new_item.html'
    login_url = "store_manager_login"
    redirect_url="store_manager_dashboard"
    redirect_field_name = "hollaback"

    def get(self, request, *args, **kwargs):
        manager_model = None
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        food_menus = restaurant_models.MenuCollection.objects.filter(manager=manager_model)
        food_addons = restaurant_models.Addons.objects.filter(manager=manager_model)
        context = {
            "food_menus" : food_menus,
            "food_addons": food_addons
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        food_name = request.POST.get('food_name')
        food_sku = request.POST.get('food_sku')
        food_description = request.POST.get('food_description')
        food_menu = request.POST.get('food_menu')
        food_addons = request.POST.getlist('food_addons')
        food_variations_IDs = request.POST.getlist('variations[]')
        print(food_menu)
        print(food_variations_IDs)
        price = int(float(request.POST.get('item_price'))*100)
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        food = restaurant_models.Food()
        food.name = food_name
        food.sku = food_sku
        food.description = food_description
        if request.method == "POST" and 'food_image' in request.FILES:
            food_image = request.FILES['food_image']
            image = image_gallery_models.Image()
            image.image_name = food_image.name
            image.image = food_image
            image.save()
            food.cover_image = image
        food.manager = manager_model
        food.amountInCents = price
        if food_menu:
            menu = restaurant_models.MenuCollection.objects.get(id=food_menu)
            food.MenuCollection = menu
        food.save()
        if food_addons:
            for food_addon in food_addons:
                if food_addon:
                    addon = restaurant_models.Addons.objects.get(id=food_addon)
                    food.addons.add(addon)
        if food_variations_IDs:
            for food_variation_ID in food_variations_IDs:
                if food_variation_ID:
                    variation = restaurant_models.FoodSubType.objects.get(id=food_variation_ID)
                    food.subtypes.add(variation)
        
        return redirect('store_manager_food_all_items')

class FoodItemUpdate(LoginRequiredMixin, IsStoreManagerMixin, TemplateView):
    template_name = "storemanagerapp/foods/update_item.html"
    login_url = "store_manager_login"
    redirect_url="store_manager_dashboard"
    redirect_field_name = "hollaback"

    def get(self, request,id, *args, **kwargs):
        manager_model = None
        try:
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            food = restaurant_models.Food.objects.get(id=id)
            food_menus = restaurant_models.MenuCollection.objects.filter(manager=manager_model)
            food_addons = restaurant_models.Addons.objects.filter(manager=manager_model)
        except Exception as e:
            manager_model = None
        context = {
            "food_menus" : food_menus,
            "food": food,
            "food_addons": food_addons
        }
        return render(request, self.template_name, context)

    def post(self, request,id, *args, **kwargs):
        food_name = request.POST.get('food_name')
        food_sku = request.POST.get('food_sku')
        food_description = request.POST.get('food_description')
        food_menu = request.POST.get('food_menu')
        food_addons = request.POST.getlist('food_addons')
        food_variations_IDs = request.POST.getlist('variations[]')
        price = int(float(request.POST.get('item_price'))*100)
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)

        food = restaurant_models.Food.objects.get(id=id)
        food.name = food_name
        food.sku = food_sku
        food.description = food_description
        if request.method == "POST" and 'food_image' in request.FILES:
            food_image = request.FILES['food_image']
            image = image_gallery_models.Image()
            image.image_name = food_image.name
            image.image = food_image
            image.save()
            food.cover_image = image
        food.manager = manager_model
        food.amountInCents = price
        if food_menu:
            menu = restaurant_models.MenuCollection.objects.get(id=food_menu)
            food.MenuCollection = menu
        food.save()
        if food_addons is not None:
            for food_addon in food_addons:
                if food_addon:
                    addon = restaurant_models.Addons.objects.get(id=food_addon)
                    food.addons.add(addon)
        if food_variations_IDs is not None and len(food_variations_IDs) > 1:
            for food_variation_ID in food_variations_IDs:
                if food_variation_ID:
                    variation = restaurant_models.FoodSubType.objects.get(id=food_variation_ID)
                    food.subtypes.add(variation)
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
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            food_menu = restaurant_models.MenuCollection.objects.get(id=id, manager=manager_model)
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
        food_items = request.POST.getlist("food_items")
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        menu = restaurant_models.MenuCollection(name=menu_name, manager=manager_model)
        menu.save()
        if food_items is not None:
            for item in food_items:
                food = restaurant_models.Food.objects.get(id=item)
                food.MenuCollection = menu
                food.save()
        return redirect('store_manager_food_all_menus')

class FoodUpdateMenu(TemplateView):
    template_name = 'storemanagerapp/foods/update_menu.html'

    def get(self, request,id,  *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        food_menu = restaurant_models.MenuCollection.objects.get(id=id, manager=manager_model)
        food_items = restaurant_models.Food.objects.all()
        selected_items = restaurant_models.Food.objects.filter(MenuCollection=food_menu, manager=manager_model)
        context = {
            "food_items": food_items,
            "food_menu":food_menu,
            "selected_items":selected_items
        }
        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        menu_name = request.POST.get("menu_name")
        food_items = request.POST.getlist("food_items")
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        menu = restaurant_models.MenuCollection.objects.get(id=id, manager=manager_model)
        if menu_name:
            menu.name = menu_name
        menu.save()
        if food_items is not None:
            for item in food_items:
                food = restaurant_models.Food.objects.get(id=item)
                food.MenuCollection = menu
                food.save()
        
        return redirect('store_manager_food_all_menus')

class FoodAllAddons(TemplateView):
    template_name = 'storemanagerapp/foods/all_addons.html'

    def get(self, request, *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        food_addons = restaurant_models.Addons.objects.filter(manager=manager_model)
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
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        addon.manager = manager_model
        addon.save()
        return redirect('store_manager_food_all_addons')

class FoodUpdateAddon(TemplateView):
    template_name = 'storemanagerapp/foods/update_addon.html'

    def get(self, request,id, *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        foodAddon = restaurant_models.Addons.objects.get(id=id, manager=manager_model)
        context = {
            "foodAddon":foodAddon
        }
        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        addon_name = request.POST.get('addon_name')
        price = float(request.POST.get('addon_price'))
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        addon = restaurant_models.Addons.objects.get(id=id, manager=manager_model)
        if addon_name:
            addon.name = addon_name
        if price:
            addon.amountInCents = int(price*100)
        addon.save()
        return redirect('store_manager_food_all_addons')

class FoodAddonDelete(TemplateView):
    def get(self, request,id, *args, **kwargs):
        try:
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            foodAddon = restaurant_models.Addons.objects.get(id=id, manager=manager_model)
            foodAddon.delete()
            return redirect('store_manager_food_all_addons')
        except Exception as e:
            return redirect('store_manager_food_all_addons')


# class FoodAllVariations(TemplateView):
#     template_name = 'storemanagerapp/foods/all_variations.html'

#     def get(self, request, *args, **kwargs):
#         variations = restaurant_models.SubType.objects.filter(manager=request.user)
#         context = {
#             "variations": variations
#         }
#         return render(request, self.template_name, context)

class FoodVariationDelete(TemplateView):
    
    def post(self, request, *args, **kwargs):
        variation_id = request.POST.get('variation_id');
        try:
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            variation = restaurant_models.SubType.objects.get(id=variation_id, manager=manager_model)
            variation.delete()
            message = {
                "message": "Variation Deleted!"
            }
            return JsonResponse(message)
        except Exception as e:
            message = {
                "message": "Failed!"
            }
            return JsonResponse(message)
    
class FoodAddNewVariation(TemplateView):
    # template_name = 'storemanagerapp/foods/add_new_variation.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        # ADD VARIATION WITH PRICE ON FOOD ADD ITEM FROM

        if request.is_ajax():
            variation_name = request.POST.get('variation_name')
            price = float(request.POST.get('variation_price'))
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            subType = restaurant_models.SubType(name=variation_name, manager=manager_model)
            subType.save()
            if subType:
                foodSubType = restaurant_models.FoodSubType(subtype=subType,amountInCents= price*100)
                foodSubType.save()
                savedFoodType = restaurant_models.FoodSubType.objects.get(id=foodSubType.pk)
                jsonResponseData = {
                    "variation_id": savedFoodType.pk,
                    "variation_name": savedFoodType.subtype.name,
                    "variation_price": savedFoodType.amountInCents
                }
                return JsonResponse(jsonResponseData)
        else:
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
        
        restaurant_address = request.POST.get('restaurant_address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        restaurant = restaurant_models.Restaurant()
        restaurant.name = restaurant_name
        restaurant.description = restaurant_description
        if request.method == "POST" and 'restaurant_image' in request.FILES:
            restaurant_image = request.FILES['restaurant_image']
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
        restaurant.manager = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        restaurant.save()
        return redirect('restaurant_all')


class RestaurantUpdate(TemplateView):
    template_name = "storemanagerapp/restaurant/update_restaurant.html"

    def get(self, request, id , *args, **kwargs):
        manager = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        restaurant = restaurant_models.Restaurant.objects.get(id=id, manager=manager)
        context = {
            "restaurant": restaurant
        }
        return render(request, self.template_name, context)

    def post(self, request, id,  *args, **kwargs):
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_description = request.POST.get('restaurant_description')
        restaurant_address = request.POST.get('restaurant_address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        manager = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)

        restaurant = restaurant_models.Restaurant.objects.get(id=id, manager=manager)
        restaurant.name = restaurant_name
        restaurant.description = restaurant_description
        if request.method == "POST" and 'restaurant_image' in request.FILES:
            restaurant_image = request.FILES['restaurant_image']
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
        restaurant.manager = manager
        
        restaurant.save()
        return redirect('restaurant_all')

class RestaurantAll(TemplateView):
    template_name = "storemanagerapp/restaurant/all_restaurant.html"

    def get(self, request, *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        restaurants = restaurant_models.Restaurant.objects.filter(manager=manager_model)
        context = {
            "restaurants": restaurants
        }
        return render(request, self.template_name, context)

class RestaurantDelete(TemplateView):
    
    def get(self, request, id,  *args, **kwargs):
        try:
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            restaurant = restaurant_models.Restaurant.objects.get(id=id, manager=manager_model)
            restaurant.delete()
            return redirect('restaurant_all')
        except Exception as e:
            return redirect('restaurant_all')

class GeneralSettings(TemplateView):
    template_name = "storemanagerapp/settings/general.html"

    def get(self, request, *args, **kwargs):
        store_manager_detail = None
        try:
            store_manager_detail = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
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
            store_manager_detail = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        except Exception as e:
            store_manager_detail = store_manager_app_models.StoreManagerBasicDetail()
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
        store_manager_detail.manager = request.user
        store_manager_detail.save()
        return redirect("settings_general")

def logoutStoreManagerUser(request):
    logout(request)
    return redirect('store_manager_dashboard')

class FoodComboAll(TemplateView):
    template_name = "storemanagerapp/foods/all_foodcombos.html"

    def get(self, request, *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        foodCombos = restaurant_models.FoodCombo.objects.filter(manager=manager_model)
        context = {
            "foodCombos": foodCombos
        }
        return render(request, self.template_name, context)

class FoodComboAddNew(TemplateView):
    template_name = "storemanagerapp/foods/add_new_foodcombo.html"

    def get(self, request, *args, **kwargs):
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        foods = restaurant_models.Food.objects.filter(manager=manager_model)
        addons = restaurant_models.Addons.objects.filter(manager=manager_model)
        context = {
            "foods": foods,
            "addons": addons
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        foodcombo_name = request.POST.get('foodcombo_name')
        foodcombo_description = request.POST.get('foodcombo_description')
        price = int(float(request.POST.get('price'))*100)
        foodcombo_addons = request.POST.getlist('foodcombo_addons')
        foodcombo_foods = request.POST.getlist('foodcombo_foods')
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)

        foodcombo = restaurant_models.FoodCombo()
        foodcombo.name = foodcombo_name
        foodcombo.description = foodcombo_description
        foodcombo.amountInCents = price
        if request.method == "POST" and 'foodcombo_image' in request.FILES:
            foodcombo_image = request.FILES['foodcombo_image']
            image = image_gallery_models.Image()
            image.image_name = foodcombo_image.name
            image.image = foodcombo_image
            image.save()
            foodcombo.cover_image = image
        foodcombo.manager = manager_model
        foodcombo.save()
        if foodcombo_addons is not None:
            for foodcombo_addon in foodcombo_addons:
                if foodcombo_addon:
                    addon = restaurant_models.Addons.objects.get(id=foodcombo_addon, manager=manager_model)
                    foodcombo.addons.add(addon)
        if foodcombo_foods is not None:
            for foodcombo_food in foodcombo_foods:
                if foodcombo_food:
                    food = restaurant_models.Food.objects.get(id=foodcombo_food, manager=manager_model)
                    foodcombo.foods.add(food)
        return redirect('store_manager_foodcombo_all')

class FoodComboDelete(TemplateView):
    def get(self, request, id,  *args, **kwargs):
        try:
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            foodcombo = restaurant_models.FoodCombo.objects.get(id=id, manager=manager_model)
            foodcombo.delete()
            return redirect('store_manager_foodcombo_all')
        except Exception as e:
            return redirect('store_manager_foodcombo_all')

class FoodComboUpdate(LoginRequiredMixin, IsStoreManagerMixin, TemplateView):
    template_name = "storemanagerapp/foods/update_foodcombo.html"
    login_url = "store_manager_login"
    redirect_url="store_manager_dashboard"
    redirect_field_name = "hollaback"

    def get(self, request,id, *args, **kwargs):
        manager_model = None
        try:
            manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
            foodCombo = restaurant_models.FoodCombo.objects.get(id=id, manager=manager_model)
            foods = restaurant_models.Food.objects.filter(manager=manager_model)
            addons = restaurant_models.Addons.objects.filter(manager=manager_model)
        except Exception as e:
            manager_model = None
        context = {
            "foodCombo" : foodCombo,
            "foods": foods,
            "addons": addons
        }
        return render(request, self.template_name, context)

    def post(self, request,id, *args, **kwargs):
        foodcombo_name = request.POST.get('foodcombo_name')
        foodcombo_description = request.POST.get('foodcombo_description')
        price = int(float(request.POST.get('price'))*100)
        foodcombo_addons = request.POST.getlist('foodcombo_addons')
        foodcombo_foods = request.POST.getlist('foodcombo_foods')
        manager_model = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)

        foodcombo = restaurant_models.FoodCombo.objects.get(id=id,manager=manager_model)
        foodcombo.name = foodcombo_name
        foodcombo.description = foodcombo_description
        foodcombo.amountInCents = price
        if request.method == "POST" and 'foodcombo_image' in request.FILES:
            foodcombo_image = request.FILES['foodcombo_image']
            image = image_gallery_models.Image()
            image.image_name = foodcombo_image.name
            image.image = foodcombo_image
            image.save()
            foodcombo.cover_image = image
        foodcombo.manager = manager_model
        foodcombo.save()
        if foodcombo_addons is not None:
            for foodcombo_addon in foodcombo_addons:
                if foodcombo_addon:
                    addon = restaurant_models.Addons.objects.get(id=foodcombo_addon, manager=manager_model)
                    foodcombo.addons.add(addon)
        if foodcombo_foods is not None:
            for foodcombo_food in foodcombo_foods:
                if foodcombo_food:
                    food = restaurant_models.Food.objects.get(id=foodcombo_food, manager=manager_model)
                    foodcombo.foods.add(food)
        return redirect('store_manager_foodcombo_all')