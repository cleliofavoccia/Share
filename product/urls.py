"""Manage product's app urls"""

from django.urls import path

from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/',
         views.ProductDetailView.as_view(),
         name='product'),
    path('supplied_products/',
         views.MySuppliedProductsListView.as_view(),
         name='supplied_products'),
    path('rented_products/',
         views.MyRentedProductsListView.as_view(),
         name='rented_products'),
    path('group/<int:pk>/add_product/',
         views.ProductInscriptionView.as_view(),
         name='add_product'),
    path('group/<int:pk>/product/<int:id>/modify_product/',
         views.ProductChangeView.as_view(),
         name='modify_product'),
    path('delete_product/',
         views.ProductSuppressionView.as_view(),
         name='delete_product'),
    path('delivery/',
         views.do_delivery,
         name='delivery'),
]
