from django.shortcuts import render
from toktok.apps.storemanagerapp.models import StoreManagerUser
from datetime import datetime, timedelta, timezone
from .models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

import jwt
from django.http import HttpResponse

my_secret = 'my_super_secret'

# Create your views here.
def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day
@csrf_exempt
def userRegister(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = request.POST.get('first_name')
        lname=request.POST.get('last_name')
        if request.method == "POST" and 'avatar' in request.FILES:
            avatar = request.FILES.get['avatar']
        user=StoreManagerUser.objects.create_user( 
        password=password, email=email)
        user_= User(manager=user,username=uname,
        first_name=fname,last_name=lname)
        user_.save()

        return HttpResponse(json.dumps({'username':uname,'firstname': fname,'lastname':lname,'email': email,'user_id': user.id}))

@csrf_exempt
def userLogin(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            payload_data = {
                "email": email,
                "password": password,
                "expired": to_integer(
            datetime.now(timezone.utc) + timedelta(hours=1))
            }
            token = jwt.encode(
                payload=payload_data, key=my_secret,algorithm='HS256')
            request.user.token = token
            return HttpResponse(json.dumps({'status':'success','email': email,'token': token}))
        else:
            return HttpResponse(json.dumps({'status':'failed'}))
        # if token=request.POST.get('token'):
        #     payload=jwt.decode(token,key=my_secret)
        #     if get_int_from_datetime(datetime.now(timezone.utc))<payload[exp]:

        
@csrf_exempt
def verifyToken(request):
    if request.method=="POST":
        token=request.POST.get('token')
       
        try:
            payload=jwt.decode(jwt=token,key=my_secret,algorithms=['HS256', ])
            if to_integer(datetime.now(timezone.utc))>payload['expired']:
                return HttpResponse(json.dumps({'status': 'failed'}))
            else:
                return HttpResponse(json.dumps({'status': 'success'}))
        except:
            return HttpResponse(json.dumps({'status': 'Token Error'}))
