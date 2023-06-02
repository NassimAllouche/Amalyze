# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, aboutus
from django.contrib.auth.views import LogoutView
from apps.authentication.views import recommendation_view , recomendationsystem , sentimentanalysis , opinionanalysiss , shippingmethodview , shippingmethod , quantitypredictionview,quantitypredict
urlpatterns = [
    path("about_us", aboutus, name="aboutus"),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('recommendation/', recommendation_view, name="recommendation"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("recomendationsystem.html", recomendationsystem, name="recomendationsystem"),
    path("sentimentanalysis/", sentimentanalysis, name="sentimentanalysis"),
    path("opinionanalysis/", opinionanalysiss, name="opinionanalysis"),
    path("shippingmethod/", shippingmethodview, name="shippingmethod"),
    path("shippingmethodpred/", shippingmethod, name="shippingmethodpred"),
    path("quantityprediction/", quantitypredictionview, name="quantityprediction"),
    path("quantitypred/", quantitypredict, name="quantitypred")

]
