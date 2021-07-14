from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from toktok.apps.orders.models import Order
from django.http import request

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
