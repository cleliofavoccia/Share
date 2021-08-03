"""Manage group_member's app urls"""

from django.urls import path

from . import views

app_name = 'group_member'
urlpatterns = [
    path('add_group_members/',
         views.GroupMemberInscription.as_view(),
         name='add_group_members'),
    path('delete_group_members/',
         views.GroupMemberUnsubscribe.as_view(),
         name='delete_group_members'),
    path('rent/',
         views.GroupMemberRental.as_view(),
         name='rent'),
    path('cancel_rent/',
         views.GroupMemberRentalAnnulation.as_view(),
         name='cancel_rent'),
]
