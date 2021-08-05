from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import unauthenticated_user


urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='store_manager_dashboard'),
    path('login/', views.StoreMangerLogin.as_view(), name='store_manager_login'),
    path('logout/', views.logoutStoreManagerUser, name='store_manager_logout')
]


foodUrlPatterns = [
    path('food/item/all', views.FoodAllItems.as_view(), name='store_manager_food_all_items'),
    path('food/item/new', views.FoodAddItemPage.as_view(), name='store_manager_food_add_new_item'),
    path('food/item/<int:id>/update', views.FoodItemUpdate.as_view(), name='store_manager_food_update_new_item'),
    path('food/item/<int:id>/delete', views.FoodItemDelete.as_view(), name='store_manager_food_delete_item'),
    # MENUS
    path('food/menu/all', views.FoodAllMenus.as_view(), name='store_manager_food_all_menus'),
    path('food/menu/<int:id>/update', views.FoodUpdateMenu.as_view(), name='store_manager_menu_update_menu'),
    path('food/menu/<int:id>/delete', views.FoodMenuDelete.as_view(), name='store_manager_menu_delete_menu'),
    path('food/menu/new', views.FoodAddNewMenu.as_view(), name='store_manager_food_add_new_menu'),

    # ADDONS
    path('food/addon/all', views.FoodAllAddons.as_view(), name='store_manager_food_all_addons'),
    path('food/addon/new', views.FoodAddNewAddon.as_view(), name='store_manager_food_add_new_addon'),
    path('food/addon/<int:id>/update', views.FoodUpdateAddon.as_view(), name='store_manager_food_update_addon'),
    path('food/addon/<int:id>/delete', views.FoodAddonDelete.as_view(), name='store_manager_food_delete_addon'),

    #VARIATIONS
    # path('food/variation/all', views.FoodAllVariations.as_view(), name='store_manager_food_all_variations'),
    path('food/variation/delete', views.FoodVariationDelete.as_view(), name='store_manager_delete_variation'),
    path('food/variation/new', views.FoodAddNewVariation.as_view(), name='store_manager_food_add_new_variation'),
    
    #FOODCOMBO
    path('food/foodcombo/all', views.FoodComboAll.as_view(), name='store_manager_foodcombo_all'),
    path('food/foodcombo/<int:id>/update', views.FoodComboUpdate.as_view(), name='store_manager_update_foodcombo'),
    path('food/foodcombo/<int:id>/delete', views.FoodComboDelete.as_view(), name='store_manager_delete_foodcombo'),
    path('food/foodcombo/new', views.FoodComboAddNew.as_view(), name='store_manager_food_add_new_foodcombo'),
]

restaurantUrlPatterns = [
    path('restaurant/new', views.RestaurantAddNew.as_view(), name= "restaurant_add_new"),
    path('restaurant/all', views.RestaurantAll.as_view(), name = "restaurant_all"),
    path('restaurant/<int:id>/update', views.RestaurantUpdate.as_view(), name = "restaurant_update"),
    path('restaurant/<int:id>/delete', views.RestaurantDelete.as_view(), name = "restaurant_delete")
]

settingsUrlPatterns = [
    path('settings/general', views.GeneralSettings.as_view(), name="settings_general")
]

urlpatterns += foodUrlPatterns
urlpatterns += restaurantUrlPatterns
urlpatterns += settingsUrlPatterns