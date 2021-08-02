"""Tests of collective_decision django views"""

from django.test import TestCase
from django.urls import reverse

from group_member.models import GroupMember
from group.models import Group
from user.models import User
from product.models import Product

from ..models import Decision


class GroupMemberDeleteVoteGroupTest(TestCase):
    """Tests on GroupMemberDeleteVoteGroup generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberDeleteVoteGroup generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberDeleteVoteGroup generic view
         and it is redirect to login form"""
        response = self.client.get(
            reverse('collective_decision:delete_vote_group')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("collective_decision:delete_vote_group")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberDeleteVoteGroup generic view's name"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)

        response = self.client.post(
            reverse('collective_decision:delete_vote_group'),
            data={'group_member': group_member.id, 'group': group.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberDeleteVoteGroup generic view
        verify datas correctly"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)
        true_request = {
            'group_member': group_member.id,
            'group': group.id
                        }
        true_response = self.client.post(
            reverse('collective_decision:delete_vote_group'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('collective_decision:vote', args=[group.id])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('collective_decision:delete_vote_group'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('index')
        )


class GroupMemberAgainstDeleteVoteGroupTest(TestCase):
    """Tests on GroupMemberAgainstDeleteVoteGroup generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test
        GroupMemberAgainstDeleteVoteGroup generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberAgainstDeleteVoteGroup generic view
        and it is redirect to login form"""
        response = self.client.get(
            reverse('collective_decision:against_delete_vote_group')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("collective_decision:against_delete_vote_group")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberAgainstDeleteVoteGroup generic view's name"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)

        response = self.client.post(
            reverse('collective_decision:against_delete_vote_group'),
            data={'group_member': group_member.id, 'group': group.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberAgainstDeleteVoteGroup generic view
        verify datas correctly"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)
        true_request = {
            'group_member': group_member.id,
            'group': group.id
                        }
        true_response = self.client.post(
            reverse('collective_decision:against_delete_vote_group'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('collective_decision:vote', args=[group.id])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('collective_decision:against_delete_vote_group'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('index')
        )


class GroupMemberModifyVoteGroupTest(TestCase):
    """Tests on GroupMemberModifyVoteGroup generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberModifyVoteGroup generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberModifyVoteGroup generic view
        and it is redirect to login form"""
        response = self.client.get(
            reverse('collective_decision:modify_vote_group')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("collective_decision:modify_vote_group")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberModifyVoteGroup generic view's name"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)

        response = self.client.post(
            reverse('collective_decision:modify_vote_group'),
            data={'group_member': group_member.id, 'group': group.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberModifyVoteGroup generic view
        verify datas correctly"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)
        true_request = {
            'group_member': group_member.id,
            'group': group.id
                        }
        true_response = self.client.post(
            reverse('collective_decision:modify_vote_group'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('collective_decision:vote', args=[group.id])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['6']
                        }
        false_response = self.client.post(
            reverse('collective_decision:modify_vote_group'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('index')
        )


class GroupMemberAgainstModifyVoteGroupTest(TestCase):
    """Tests on GroupMemberAgainstModifyVoteGroup generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test
        GroupMemberAgainstModifyVoteGroup generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupMemberAgainstModifyVoteGroup generic view
        and it is redirect to login form"""
        response = self.client.get(
            reverse('collective_decision:against_modify_vote_group')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("collective_decision:against_modify_vote_group")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupMemberAgainstModifyVoteGroup generic view's name"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)

        response = self.client.post(
            reverse('collective_decision:against_modify_vote_group'),
            data={'group_member': group_member.id, 'group': group.id}
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupMemberAgainstModifyVoteGroup generic view
        verify datas correctly"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)
        true_request = {
            'group_member': group_member.id,
            'group': group.id
                        }
        true_response = self.client.post(
            reverse('collective_decision:against_modify_vote_group'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('collective_decision:vote', args=[group.id])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('collective_decision:against_modify_vote_group'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('index')
        )


class GroupVoteViewTest(TestCase):
    """Tests on GroupVoteView generic detail view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test GroupVoteView generic detail view"""
        cls.user1 = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.user2 = User.objects.create_user(
            username='Sam',
            email='sam@gmail.com',
            password='frodon'
        )

        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member1 = GroupMember.objects.create(
            user=cls.user1,
            group=cls.group
        )
        cls.group_member2 = GroupMember.objects.create(
            user=cls.user2,
            group=cls.group
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to GroupVoteView generic view
        and it is redirect to login form"""
        group = Group.objects.get(name="La communauté de l'anneau")
        response = self.client.get(
            reverse("collective_decision:vote", args=[group.pk])
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("collective_decision:vote", args=[group.pk])}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by GroupVoteView
        generic detail view's name"""
        self.client.force_login(self.user1)
        group = Group.objects.get(name="La communauté de l'anneau")

        response = self.client.get(
            reverse('collective_decision:vote', args=[group.id])
        )
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test GroupVoteView use the correct template"""
        self.client.force_login(self.user1)
        group = Group.objects.get(name="La communauté de l'anneau")
        response = self.client.get(
            reverse('collective_decision:vote', args=[group.id])
        )

        self.assertTemplateUsed(response, 'collective_decision/vote.html')

    def test_group_modification_is_true_if_users_are_voted_for(self):
        """Test users can modify group if all users
        are voted for modification"""
        self.client.force_login(self.user1)
        user1 = User.objects.get(username='Frodon')
        user2 = User.objects.get(username='Sam')
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member1 = GroupMember.objects.get(user=user1, group=group)
        group_member2 = GroupMember.objects.get(user=user2, group=group)

        Decision.objects.create(
            group=group,
            group_member=group_member1,
            modify_group_vote=True
        )
        Decision.objects.create(
            group=group,
            group_member=group_member2,
            modify_group_vote=True
        )

        response = self.client.get(
            reverse('collective_decision:vote', args=[group.id])
        )

        self.assertTrue(response.context['modification_group_activate'])

    def test_group_is_deleted_if_users_are_voted_for_suppression(self):
        """Test group is deleted if all users are voted for suppression"""
        self.client.force_login(self.user1)
        user1 = User.objects.get(username='Frodon')
        user2 = User.objects.get(username='Sam')
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member1 = GroupMember.objects.get(user=user1, group=group)
        group_member2 = GroupMember.objects.get(user=user2, group=group)

        Decision.objects.create(
            group=group,
            group_member=group_member1,
            delete_group_vote=True
        )
        Decision.objects.create(
            group=group,
            group_member=group_member2,
            delete_group_vote=True
        )

        response = self.client.get(
            reverse('collective_decision:vote', args=[group.id])
        )

        self.assertEqual(
            response.context['delete'],
            'La communauté a bien été supprimé'
        )

        # Verify if community is well deleted in database
        self.assertRaises(
            Group.DoesNotExist,
            Group.objects.get,
            name="La communauté de l'anneau"
        )


class CostEstimationViewTest(TestCase):
    """Tests on CostEstimationView generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test CostEstimationView generic view"""

        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

        cls.product = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            tenant=cls.group_member,
            group=cls.group,
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to CostEstimationView generic view
         and it is redirect to login form"""

        product = Product.objects.get(name="Epée")

        response = self.client.get(
            reverse('collective_decision:estimation', args=[product.pk])
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next='
            f'{reverse("collective_decision:estimation", args=[product.pk])}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        CostEstimationView generic view's name"""

        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        product = Product.objects.get(name="Epée")

        get_response = self.client.get(
            reverse("collective_decision:estimation", args=[product.pk]),
        )

        post_response = self.client.post(
            reverse("collective_decision:estimation", args=[product.pk]),
            data={
                'csrfmiddlewaretoken':
                    ['2NFhGPdsobAfUWtJZFxBnkUL7uSdSe5hj'
                     '17l20tZbFZaLtxaTbx9NbKaZDfwTMfU'],
                'cost': ['25']
            }
        )

        # Check that we got a response "success"
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test CostEstimationView generic view
        verify datas correctly"""

        self.client.force_login(self.user)
        product = Product.objects.get(name="Epée")

        true_request = {
                'csrfmiddlewaretoken':
                ['2NFhGPdsobAfUWtJZFxBnkUL7uSdSe5hj'
                    '17l20tZbFZaLtxaTbx9NbKaZDfwTMfU'],
                'cost': ['25']
            }
        true_response = self.client.post(
            reverse("collective_decision:estimation", args=[product.pk]),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse("product:product", args=[product.pk])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse("collective_decision:estimation", args=[product.pk]),
            data=false_request
        )

        self.assertEqual(
            false_response.status_code,
            200
        )
