"""Tests of group_member django views"""

from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from group.models import Group
from user.models import User
from product.models import Product

from ..models import GroupMember


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

        try:
            self.client.post(
                reverse('group_member:add_group_members'),
                data=false_request
            )
        except NoReverseMatch:
            self.assertRaises(NoReverseMatch)


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
            'user': ['2'],
            'group': ['Y'],
        }

        try:
            self.client.post(
                reverse('group_member:delete_group_members'),
                data=false_request
            )
        except NoReverseMatch:
            self.assertRaises(NoReverseMatch)


class GroupMemberRentalTest(TestCase):
    """Tests on GroupMemberRental generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberRental generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group,
            points_posseded=15

        )

        cls.product = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            group=cls.group,
            points=10
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberRental generic view
         and it is redirect to login form"""
        response = self.client.get(
            reverse('group_member:rent')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("group_member:rent")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberRental generic view's name"""

        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )

        product = Product.objects.get(name='Epée')

        self.client.force_login(user)

        response = self.client.post(
            reverse('group_member:rent'),
            data={
                'group_member': group_member.id,
                'product': product.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberRental generic view
        verify datas correctly"""

        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )

        product = Product.objects.get(name='Epée')

        self.client.force_login(user)

        true_request = {
            'group_member': group_member.id,
            'product': product.id
                        }
        true_response = self.client.post(
            reverse('group_member:rent'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('product:product', args=[product.pk])
        )

        false_request = {
            'group_member': ['1'],
            'product': ['Y']
                        }

        try:
            self.client.post(
                reverse('group_member:rent'),
                data=false_request
            )
        except NoReverseMatch:
            self.assertRaises(NoReverseMatch)
