from django.urls import path
from .views import Explorer, MyCommunities

app_name = 'dashboard'
urlpatterns = [
    path('', Explorer.as_view(), name='explorer'),
    path('my_communities', MyCommunities.as_view(), name='my_communities'),
]
