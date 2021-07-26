"""Manage group's app urls"""

from django.urls import path

from . import views

app_name = 'group'
urlpatterns = [
    path('<int:pk>/',
         views.CommunityDetailView.as_view(),
         name='community'),
    path('group_inscription/',
         views.GroupInscriptionView.as_view(),
         name='group_inscription'),
    path('modify_group/<int:pk>/',
         views.GroupChangeView.as_view(),
         name='modify_group'),
    ]
