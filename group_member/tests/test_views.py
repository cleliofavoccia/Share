"""Tests of group_member django views"""

from django.test import TestCase
from django.urls import reverse

from group.models import Group
from user.models import User


class GroupMemberInscriptionTest(TestCase):
    """Tests on GroupMemberInscription generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberInscription generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberInscription generic view
         and it is redirect to login form"""
        response = self.client.get(
            reverse('group_member:add_group_members')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("group_member:add_group_members")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberInscription generic view's name"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        self.client.force_login(user)

        response = self.client.post(
            reverse('group_member:add_group_members'),
            data={'user': user.id, 'group': group.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberInscription generic view
        verify datas correctly"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        self.client.force_login(user)

        true_request = {
            'user': user.id,
            'group': group.id
                        }
        true_response = self.client.post(
            reverse('group_member:add_group_members'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('group:community', args=[group.pk])
        )

        false_request = {
            'user': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('group_member:add_group_members'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('website:fail')
        )


class GroupMemberUnsubscribeTest(TestCase):
    """Tests on GroupMemberUnsubscribe generic view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberUnsubscribe generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberUnsubscribe generic view
         and it is redirect to login form"""
        response = self.client.get(
            reverse('group_member:delete_group_members')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("group_member:delete_group_members")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberUnsubscribe generic view's name"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        self.client.force_login(user)

        response = self.client.post(
            reverse('group_member:delete_group_members'),
            data={'user': user.id, 'group': group.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberUnsubscribe generic view
        verify datas correctly"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        self.client.force_login(user)

        true_request = {
            'user': user.id,
            'group': group.id
        }
        true_response = self.client.post(
            reverse('group_member:delete_group_members'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('group:community', args=[group.id])
        )

        false_request = {
            'user': ['1'],
            'group': ['Y']
        }
        false_response = self.client.post(
            reverse('group_member:delete_group_members'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('website:fail')
        )
