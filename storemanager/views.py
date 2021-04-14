from django.shortcuts import render
from django.views.generic import TemplateView

class StoreManagerApp(TemplateView):
    def get(self, request, *args, **kwargs):
        pass

