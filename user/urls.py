"""Manage user's app urls"""

from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('my_account/', views.UserDetailView.as_view(), name='account')
    ]
