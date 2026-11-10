from django.shortcuts import render 
from django.http import HttpResponse
from datetime import datetime

def home(request):
    path=request.path
    scheme=request.scheme
    method=request.method
    address=request.META['REMOTE_ADDR']
    user_agent=request.META['HTTP_USER_AGENT']
    path_info=request.path_info

    response=HttpResponse(msg)
    response.headers['Age']=20
    msg={f"""
         <br>path:{path}
         <br>Address:{address}
         <br>Scheme:{scheme}
         <br>Method:{method}
         <br>User agent:{user_agent}
         <br>path info:{path_info}
         <br>Response header:{response.headers}

    """
    }
    response= HttpResponse(msg)
    response.headers['Age']=20
    return response
# Create your views here.
def say_hello(request):
    return HttpResponse ("Hello Aisha")

def homepage(request):
    return HttpResponse("welcom Aisha")

def display_date(request):
    date_joined =datetime.today().year
    return HttpResponse(date_joined)

def menuitems(request,dish):
    items={
        'pasta':'is noodle',
        'falafel':'are deep fried',
        'chesecake':'type of desert'
    }
    discription =items[dish]
    return HttpResponse(f"<h2>{dish}</h2>"+discription)