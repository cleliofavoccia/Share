"""URLS of products app"""
from django.urls import path

from . import views

app_name = 'group_member'
urlpatterns = [
    path('add_group_members/', views.GroupMemberInscription.as_view(), name='add_group_members'),
    path('delete_group_members/', views.GroupMemberDesinscription.as_view(), name='delete_group_members'),
    path('fail/', views.FailView.as_view(), name='fail'),
    path('well_done/', views.WellDoneView.as_view(), name='well_done'),
    ]
