"""Manage collective_decision app urls"""

from django.urls import path

from . import views

app_name = 'collective_decision'

urlpatterns = [
    path('delete_vote_group/',
         views.GroupMemberDeleteVoteGroup.as_view(),
         name='delete_vote_group'),
    path('against_delete_vote_group/',
         views.GroupMemberAgainstDeleteVoteGroup.as_view(),
         name='against_delete_vote_group'),
    path('modify_vote_group/',
         views.GroupMemberModifyVoteGroup.as_view(),
         name='modify_vote_group'),
    path('against_modify_vote_group/',
         views.GroupMemberAgainstModifyVoteGroup.as_view(),
         name='against_modify_vote_group'),
    path('vote/<int:pk>', views.GroupVoteView.as_view(), name='vote'),
    path('estimation/<int:pk>/',
         views.CostEstimationView.as_view(),
         name='estimation'
         ),
]
