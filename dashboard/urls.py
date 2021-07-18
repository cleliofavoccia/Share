from django.urls import path
from .views import Explorer, MyCommunities

urlpatterns = [
    path('', Explorer.as_view(), name='explorer'),
    path('explorer', Explorer.as_view(), name='explorer'),
    path('my_communities', MyCommunities.as_view(), name='my_communities'),
]
