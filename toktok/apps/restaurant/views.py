from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FoodCombo
from toktok.apps.restaurant.models import Food
from toktok.apps.imagegallery.models import Image

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