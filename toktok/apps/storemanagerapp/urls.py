from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import unauthenticated_user


urlpatterns = [
    path('', views.Dashboard.as_view(), name='store_manager_dashboard'),
    path('login/', views.StoreMangerLogin.as_view(), name='store_manager_login'),
    path('logout/', views.logoutStoreManagerUser, name='store_manager_logout')
]


foodUrlPatterns = [
    path('food/item/all', views.FoodAllItems.as_view(), name='store_manager_food_all_items'),
    path('food/item/new', views.FoodAddItemPage.as_view(), name='store_manager_food_add_new_item'),
    path('food/item/<int:id>/delete', views.FoodItemDelete.as_view(), name='store_manager_food_delete_item'),
    path('food/menu/all', views.FoodAllMenus.as_view(), name='store_manager_food_all_menus'),
    path('food/menu/<int:id>/delete', views.FoodMenuDelete.as_view(), name='store_manager_menu_delete_item'),
    path('food/addon/all', views.FoodAllAddons.as_view(), name='store_manager_food_all_addons'),
    path('food/menu/new', views.FoodAddNewMenu.as_view(), name='store_manager_food_add_new_menu'),
    path('food/addon/new', views.FoodAddNewAddon.as_view(), name='store_manager_food_add_new_addon'),
    path('food/variation/all', views.FoodAllVariations.as_view(), name='store_manager_food_all_variations'),
    path('food/variation/<int:id>/delete', views.FoodVariationDelete.as_view(), name='store_manager_menu_delete_item'),
    path('food/variation/new', views.FoodAddNewVariation.as_view(), name='store_manager_food_add_new_variation')
]

restaurantUrlPatterns = [
    path('restaurant/new', views.RestaurantAddNew.as_view(), name= "restaurant_add_new"),
    path('restaurant/', views.RestaurantAll.as_view(), name = "restaurant_all")
]

settingsUrlPatterns = [
    path('settings/general', views.GeneralSettings.as_view(), name="settings_general")
]

urlpatterns += foodUrlPatterns
urlpatterns += restaurantUrlPatterns
urlpatterns += settingsUrlPatterns