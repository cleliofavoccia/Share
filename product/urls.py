"""URLS of products app"""
from django.urls import path

from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('mes_produits_fournis/', views.MySuppliedProductsListView.as_view(), name='mes_produits_fournis'),
    ]
