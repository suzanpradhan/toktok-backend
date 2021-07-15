from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from toktok.apps.orders.models import Order
from django.http import HttpResponse, request
from toktok.apps.basicapp.models import Location
from toktok.apps.customer.models import User
from django.views.decorators.csrf import csrf_exempt
import json

class Allorders(TemplateView):
    template_name = "orders/allorders.html"

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        context = {
            "orders": orders
        }
        return render(request, self.template_name, context)

    def post(self, request,*args, **kwargs):
        if request.POST.get('accepted'):
            order = Order.objects.get(id=request.POST.get('id'))
            order.manager = request.user
            order.save

class Myorder(TemplateView):
    template_name = "orders/myorders.html"

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(manager=request.user)
        context = {
            "orders": orders
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=request.POST.get('id'))
        order.choice=request.POST.get('choice')

def createOrder(request):
    if request.method == 'POST':
        try:
            order=Order
            manager_ = request.user
            foods_=request.POST.getlist("foods")
            restaurant_=request.POST.get("restaurant")
            address_=request.POST.get('address')
            long_=request.POST.get('longitude')
            lat_=request.POST.get('longitude')
            amount=request.POST.get('amount')
            orderTime=request.POST.get('orderTime')
            deliveryTime=request.POST.get('deliveryTime')

            for food in foods_:
                if food:
                    order.foods.add(restaurant_models.Food.get(id=food))

            if restaurant_:
                restaurant = restaurant_models.Restaurant.get(id=restaurant_)
                order.restaurant=restaurant

            if address_ and long_ and lat_:
                location = Location(name=address_,longitude=long_,latitude=lat_)
                order.location=location
            
            if amount:
                order.totalAmount=amount
            
            if orderTime:
                order.orderTime = orderTime
            
            if deliveryTime:
                order.deliveryTime = deliveryTime
            
            order.save()

            foodList=[]
            for food in order.foods.all():
                foodList.append(food.id)
            data={
                    'manager':order.manager.id,
                    'foods':foodList,
                    'restaurant':order.restaurant.id,
                    'location':{'address':order.location.name,'longitude':order.location.longitude,'latitude':order.location.latitude},
                    'totalAmount':order.totalAmount,
                    'orderTime':str(order.orderTime),
                    'deliveryTime':str(order.deliveryTime),
                    'orderstatus':order.status,
                    'status':"Success"}
            return HttpResponse(json.dumps(data))
        except :
            return HttpResponse(json.dump({'status':"Error Status 200"}))

@csrf_exempt
def getUserOrder(request):
    if request.method=="POST":
        user = User.objects.get(id=request.POST.get('id'))
        orders=Order.objects.filter(manager=user)
        list=[]
        foodList=[]
        for order in orders:
            for food in order.foods.all():
                foodList.append(food.id)
            data={
                'manager':order.manager.id,
                'foods':foodList,
                'restaurant':order.restaurant.id,
                'location':{'address':order.location.name,'longitude':order.location.longitude,'latitude':order.location.latitude},
                'totalAmount':order.totalAmount,
                'orderTime':str(order.orderTime),
                'deliveryTime':str(order.deliveryTime),
                'status':order.status
            }
            list.append(data)
        return HttpResponse(json.dumps(list))

@csrf_exempt
def getAllOrder(request):
    if request.method=="GET":
        orders=Order.objects.all()
        list=[]
        foodList=[]
        for order in orders:
            for food in order.foods.all():
                foodList.append(food.id)
            data={
                'manager':order.manager.id,
                'foods':foodList,
                'restaurant':order.restaurant.id,
                'location':{'address':order.location.name,'longitude':order.location.longitude,'latitude':order.location.latitude},
                'totalAmount':order.totalAmount,
                'orderTime':str(order.orderTime),
                'deliveryTime':str(order.deliveryTime),
                'status':order.status
            }
            list.append(data)
        return HttpResponse(json.dumps(list))

@csrf_exempt
def getOrder(request):
    if request.method=="POST":
        order=Order.objects.get(id=request.POST.get('id'))
        foodList=[]
        for food in order.foods.all():
            foodList.append(food.id)
        data={
                'manager':order.manager.id,
                'foods':foodList,
                'restaurant':order.restaurant.id,
                'location':{'address':order.location.name,'longitude':order.location.longitude,'latitude':order.location.latitude},
                'totalAmount':order.totalAmount,
                'orderTime':str(order.orderTime),
                'deliveryTime':str(order.deliveryTime),
                'status':order.status}
        return HttpResponse(json.dumps(data))

# @csrf_exempt
# def changeStatus(request):
#     if request.method=="GET":
