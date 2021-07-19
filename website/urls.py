"""URLS of products app"""
from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('fail/', views.FailView.as_view(), name='fail')
    ]
