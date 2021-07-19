"""Manage group's app urls"""

from django.urls import path

from . import views

app_name = 'group'
urlpatterns = [
    path('<int:pk>/',
         views.CommunityDetailView.as_view(),
         name='community'),
    path('<int:pk>/inscrire_produit/',
         views.ProductInscriptionView.as_view(),
         name='inscrire_produit'),
    path('inscrire_groupe/',
         views.GroupInscriptionView.as_view(),
         name='group_inscription'),
    ]
