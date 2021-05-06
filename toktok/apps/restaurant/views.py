from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FoodCombo
from toktok.apps.restaurant.models import Food, MenuCollection
from toktok.apps.imagegallery.models import Image
import pandas as pd
from toktok.apps.storemanagerapp.models import StoreManagerBasicDetail

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
        