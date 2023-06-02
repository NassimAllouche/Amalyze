# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
import json
import pandas as pd
from django.http import JsonResponse
from apps.recommender.recomendationsystem import get_recommandation
from apps.sentimentanalysis.sentimentanalysis import ekman_classifier
from apps.opinionanalysis.opinionanalysis import opinionanalysis
from apps.shippingmethod.shippingmethod import predict_fulfilled_by
from apps.quantityprediction.quantityprediction import predict_qty
from django.core.serializers import serialize


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Incorrect username or password'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Invalid credential'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def aboutus(request):
    return render(request, "accounts/aboutus.html")

def recomendationsystem(request):
    d= pd.read_csv('C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/recommender/recommandation.csv' ,delimiter= ';')
    data = d[['Product_Name']].iloc[:1000, :]
    print(data)
    return render( request,"home/recomendationsystem.html" , {"data": data.drop_duplicates()} )

def recommendation_view(request):
  
        titre = str(request.POST.get('titre'))
        recommendations = get_recommandation(titre) 
        return JsonResponse({'recommendations': recommendations})
    
def sentimentanalysis (request):
  
        titre = str(request.POST.get('titre'))
        emotion = ekman_classifier(titre) 
        return JsonResponse({'emotion': emotion})
def opinionanalysiss (request):
  
        titre = request.POST.get('titre')
        emotion = opinionanalysis(titre) 
        return JsonResponse({'emotion': emotion})
def shippingmethodview(request):
    d= pd.read_csv('C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/shippingmethod/Amazon Sale Report 3 (1).csv' ,delimiter= ';')
    courierstatus = d[['Courier Status']].iloc[:200000, :]
    category = d[['Category']].iloc[:200000, :]
    qty = d[['Qty']].iloc[:200000, :]
    amount = d[['Amount']].iloc[:20000, :]
    print(qty , amount , category.drop_duplicates() , courierstatus)
    return render( request,"home/shippingmethod.html" , {"courierstatus": courierstatus['Courier Status'].drop_duplicates(), "category": category.drop_duplicates(), "qty": qty.drop_duplicates(), "amount": amount.drop_duplicates()} )

def shippingmethod(request):

    amount =  float(request.POST.get('amount'))
    qty = float(request.POST.get('qty'))
    courierstatus = float(request.POST.get('courierstatus'))
    category = float(request.POST.get('category'))

    prediction = predict_fulfilled_by(category,courierstatus,amount,qty)
    return JsonResponse({'prediction': prediction})

def quantitypredictionview(request):
    d= pd.read_csv('C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/quantityprediction/Amazon Sale Report.csv' ,delimiter= ';')
    fulfilment = d[['Fulfilment']].iloc[:200000, :]
    fulfilledby = d[['fulfilled-by']].iloc[:200000, :]
    shipservicelevel = d[['ship-service-level']].iloc[:200000, :]
    courierstatus = d[['Courier Status']].iloc[:200000, :]
    category = d[['Category']].iloc[:200000, :]
    print(category)
    return render( request,"home/quantityprediction.html" , {"courierstatus": courierstatus['Courier Status'].drop_duplicates(), "category": category.drop_duplicates(), "fulfilment": fulfilment['Fulfilment'].drop_duplicates(), "fulfilledby": fulfilledby['fulfilled-by'].drop_duplicates(), "shipservicelevel": shipservicelevel['ship-service-level'].drop_duplicates()} )


def quantitypredict(request):

    fulfilment =  request.POST.get('fulfilment')
    fulfilledby = request.POST.get('fulfilledby')
    shipservicelevel = request.POST.get('shipservicelevel')
    courierstatus = request.POST.get('courierstatus')
    category = request.POST.get('category')

    prediction = predict_qty(fulfilment,fulfilledby,shipservicelevel,courierstatus,category)
    return JsonResponse({'prediction': prediction})