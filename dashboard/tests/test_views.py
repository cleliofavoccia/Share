"""Tests of dashboard django views"""
from django.test import TestCase
from django.urls import reverse

from group_member.models import GroupMember
from group.models import Group
from user.models import User


class ExplorerTest(TestCase):
    """Test on Explorer object generic Group list view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test Explorer generic Group list view"""
        cls.user1 = User.objects.create_user(username='Frodon', email='frodon@gmail.com', password='sam')
        cls.group1 = Group.objects.create(name="La communauté de l'anneau")
        cls.group2 = Group.objects.create(name="Mordor")

        cls.group1_member1 = GroupMember.objects.create(user=cls.user1, group=cls.group1)
        cls.group2_member1 = GroupMember.objects.create(user=cls.user1, group=cls.group2)

    def test_view_uses_correct_template(self):
        """Test Explorer use the correct template"""
        response = self.client.get(reverse('dashboard:explorer'))

        self.assertTemplateUsed(response, 'dashboard/templates/dashboard/explorer.html')

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by FailView generic view's name"""
        response = self.client.get(reverse('dashboard:explorer'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_view_print_all_communities_where_user_has_suscribed(self):

        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard:explorer'))

        user_communities = list()
        group_member = GroupMember.objects.filter(user=user)
        for community in group_member:
            user_communities.append(community.group.name)

        self.assertEqual(response.context['group_member_list'], user_communities)



