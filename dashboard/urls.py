from django.urls import path
from .views import Dashboard, Example

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('example', Example.as_view(), name='example'),
]
