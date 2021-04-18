from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='store_manager_dashboard'),
    path('login/', views.StoreMangerLogin.as_view(), name='store_manager_login'),
]


foodUrlPatterns = [
    path('food/item/', views.FoodAllItems.as_view(), name='store_manager_food_all_items'),
    path('food/item/new', views.FoodAddItemPage.as_view(), name='store_manager_food_add_new_item'),
    path('food/menu/', views.FoodAllMenus.as_view(), name='store_manager_food_all_menus'),
    path('food/menu/new', views.FoodAddNewMenu.as_view(), name='store_manager_food_add_new_menu'),
    path('food/addon/new', views.FoodAddNewAddon.as_view(), name='store_manager_food_add_new_addon'),
    path('food/variation/new', views.FoodAddNewVariation.as_view(), name='store_manager_food_add_new_variation')
]

urlpatterns += foodUrlPatterns