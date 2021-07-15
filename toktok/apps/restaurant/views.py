from django.shortcuts import render
from django.views.generic import TemplateView
# from .models import FoodCombo
from toktok.apps.restaurant.models import Food, MenuCollection, Restaurant
from toktok.apps.imagegallery.models import Image
import pandas as pd
from toktok.apps.storemanagerapp.models import StoreManagerBasicDetail
from django.http import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

class AddUpdateFoodCombo(TemplateView):
    def post(self, request, id,*args,**kwargs):
        name = request.POST.get('name')
        foods = request.POST.get('foods')
        priceInCents = request.POST.get('price')
        image = request.FILES.get('image')

        try:
            combo = FoodCombo.objects.get(id=id)
            if name:
                combo.name = name
            if foods:
                obj=[]
                for _ in foods:
                    obj.append(Food.objects.get(id=_))
                combo.foods=obj
            if priceInCents:
                combo.priceInCents=priceInCents
            if image:
                combo.image = Image.objects.get(id=image)
            combo.save()
        
        except :
            obj=[]
            for _ in foods:
                obj.append(Food.objects.get(id=_))
            
            combo = FoodCombo(name = request.POST.get('name'),
                                foods = obj,
                                priceInCents = request.POST.get('price'),
                                image = Image.objects.get(id=image))
            combo.save()
    
    def get(self):
        foodCombo = FoodCombo.objects.all()
        return foodCombo


class DeleteFoodCombo(TemplateView):
    def post(self, request, id,*args,**kwargs):
        FoodCombo.objects.filter(id=id).delete()

class excelImport(TemplateView):

    def post(self, request,*args,**kwargs):
        df = pd.read_excel (r'D:\work\Django\toktok-backend\toktok\apps\restaurant\product_1618567151_sample_mcdonalds.xls')
        for _ in range(len(df)):
            name=df.iloc[_][1]
            sku=df.iloc[_][3]
            description=df.iloc[_][2]
            cover_image=df.iloc[_][7]
            manager=StoreManagerBasicDetail.objects.get(manager=request.user)
            amountInCents = df.iloc[_][6]
            MenuColl=df.iloc[_][0]
            subtype=df.iloc[_][8]
            addons=None
            try:
                menuCollection = MenuCollection.objects.get(name=MenuColl)
            except:
                menuCollection = MenuCollection(name=MenuColl,manager=manager)
                menuCollection.save()
            
            print(name,sku,description,cover_image,manager,amountInCents,MenuColl,subtype,addons)
            print("\n")

def getAllFood(request):
    if request.method=="GET":
        foods=[]
        allFood=Food.objects.all()
        subtypes=[]
        addons=[]
        for food in allFood:
            for type in food.subtypes.all():
                subtype={'name':type.subtype.name,'manager':type.subtype.manager.id,'amount':type.amountInCents}
                subtypes.append(subtype)
            for add in food.addons.all():
                addon={'name':add.name,'amount':add.amountInCents,'description':add.description,'manager':add.manager.id}
                addons.append(addon)
            if food.cover_image:
                imageUrl=food.cover_image.image.url
            else:
                imageUrl=None
            data={
                'name':food.name,
                'sku':food.sku,
                'description':food.description,
                'imageURL':imageUrl,
                'manager':food.manager.id,
                'amountInCents':food.amountInCents,
                'menuCollection':{'name':food.MenuCollection.name,'manager':food.MenuCollection.manager.id},
                'subTypes':subtypes,
                'addons':addons
            }
            foods.append(data)
        return HttpResponse(json.dumps(foods))

def getAllRestaurant(request):
    if request.method=="GET":
        restaurants=[]
        for restaurant in Restaurant.objects.all():
            if restaurant.cover_image:
                imageUrl=restaurant.cover_image.image.url
            else:
                imageUrl=None
            data={
                'name':restaurant.name,
                'description':restaurant.description,
                'imageURL':imageUrl,
                'address':restaurant.location.name,
                'lat':restaurant.location.latitude,
                'long':restaurant.location.longitude,
                'manager':restaurant.manager.id
            }
            restaurants.append(data)

        return HttpResponse(json.dumps(restaurants))

@csrf_exempt
def searchFood(request):
    if request.method=="POST":
        foods=[]
        subtypes=[]
        addons=[]
        for food in Food.objects.filter(name__startswith=request.POST.get("value")):
            for type in food.subtypes.all():
                subtype={'name':type.subtype.name,'manager':type.subtype.manager.id,'amount':type.amountInCents}
                subtypes.append(subtype)
            for add in food.addons.all():
                addon={'name':add.name,'amount':add.amountInCents,'description':add.description,'manager':add.manager.id}
                addons.append(addon)
            if food.cover_image:
                imageUrl=food.cover_image.image.url
            else:
                imageUrl=None
            data={
                'name':food.name,
                'sku':food.sku,
                'description':food.description,
                'imageURL':imageUrl,
                'manager':food.manager.id,
                'amountInCents':food.amountInCents,
                'menuCollection':{'name':food.MenuCollection.name,'manager':food.MenuCollection.manager.id},
                'subTypes':subtypes,
                'addons':addons
            }
            foods.append(data)
        return HttpResponse(json.dumps(foods))
@csrf_exempt
def searchRestaurant(request):
    if request.method=="POST":
        restaurants=[]
        for restaurant in  Restaurant.objects.filter(name__startswith=request.POST.get("value")):
            if restaurant.cover_image:
                imageUrl=restaurant.cover_image.image.url
            else:
                imageUrl=None
            data={
                'name':restaurant.name,
                'description':restaurant.description,
                'imageURL':imageUrl,
                'address':restaurant.location.name,
                'lat':restaurant.location.latitude,
                'long':restaurant.location.longitude,
                'manager':restaurant.manager.id
            }
            restaurants.append(data)

        return HttpResponse(json.dumps(restaurants))

@csrf_exempt
def getFood(request):
    if request.method=="POST":
        subtypes=[]
        addons=[]
        food = Food.objects.get(pk=request.POST.get("value"))
        for type in food.subtypes.all():
            subtype={'name':type.subtype.name,'manager':type.subtype.manager.id,'amount':type.amountInCents}
            subtypes.append(subtype)
        for add in food.addons.all():
            addon={'name':add.name,'amount':add.amountInCents,'description':add.description,'manager':add.manager.id}
            addons.append(addon)
        if food.cover_image:
            imageUrl=food.cover_image.image.url
        else:
            imageUrl=None
        data={
                'name':food.name,
                'sku':food.sku,
                'description':food.description,
                'imageURL':imageUrl,
                'manager':food.manager.id,
                'amountInCents':food.amountInCents,
                'menuCollection':{'name':food.MenuCollection.name,'manager':food.MenuCollection.manager.id},
                'subTypes':subtypes,
                'addons':addons
            }
        return HttpResponse(json.dumps([data]))
        

@csrf_exempt
def getRestaurant(request):
    if request.method=="POST":
        restaurant = Restaurant.objects.get(pk=request.POST.get("value"))
        if restaurant.cover_image:
                imageUrl=restaurant.cover_image.image.url
        else:
                imageUrl=None
        data={
                'name':restaurant.name,
                'description':restaurant.description,
                'imageURL':imageUrl,
                'address':restaurant.location.name,
                'lat':restaurant.location.latitude,
                'long':restaurant.location.longitude,
                'manager':restaurant.manager.id
            }
        return HttpResponse(json.dumps([data]))
