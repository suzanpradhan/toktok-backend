from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from django.shortcuts import render
from django.views.generic import TemplateView
# from .models import FoodCombo
from toktok.apps.restaurant.models import Food, MenuCollection, Restaurant
from toktok.apps.imagegallery.models import Image
import pandas as pd
from toktok.apps.storemanagerapp.models import StoreManagerBasicDetail
from django.http import HttpResponse, response
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .searializers import FoodSerializer

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
        test = []
        for food in Food.objects.all():
            foods.append(food)
        # food =serializers.serialize("json", foods)
        responseData = FoodSerializer
        return HttpResponse(food)

def getAllRestaurant(request):
    if request.method=="GET":
        restaurants=[]
        for restaurant in Restaurant.objects.all():
            restaurants.append(restaurant)
        restaurant =serializers.serialize("json", restaurants)
        return HttpResponse(restaurant)

@csrf_exempt
def searchFood(request):
    if request.method=="POST":
        
        foods=[]
        for food in Food.objects.filter(name__startswith=request.POST.get("value")):
            foods.append(food)

        food =serializers.serialize("json", foods)
        return HttpResponse(food)

@csrf_exempt
def searchRestaurant(request):
    if request.method=="POST":
        restaurants=[]
        for restaurant in Restaurant.objects.filter(name__startswith=request.POST.get("value")):
            restaurant.url=restaurant.cover_image.image.url
            restaurants.append(restaurant)
        restaurant =serializers.serialize("json", restaurants)
        return HttpResponse(restaurant)

@csrf_exempt
def getFood(request):
    if request.method=="POST":
        food = [Food.objects.get(pk=request.POST.get("value"))]
        foods = serializers.serialize("json", food)
        split=foods.split('{')
        data='image_url: '+str(food[0].cover_image.image.url)+','
        split[2]=data+split[2]
        foods='{'.join(split)
        return HttpResponse(foods)

@csrf_exempt
def getRestaurant(request):
    if request.method=="POST":
        restaurant = [Restaurant.objects.get(pk=request.POST.get("value"))]
        restaurants = serializers.serialize("json", restaurant)
        split=restaurants.split('{')
        data='image_url: '+str(restaurant[0].cover_image.image.url)+','
        split[2]=data+split[2]
        foods='{'.join(split)
        return HttpResponse(restaurants)
