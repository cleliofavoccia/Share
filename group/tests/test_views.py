"""Tests of group django views"""

from django.test import TestCase
from django.urls import reverse

from group_member.models import GroupMember
from user.models import User
from collective_decision.models import Decision

from ..models import Group


class CommunityDetailViewTest(TestCase):
    """Tests on CommunityDetailView generic detail view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test CommunityDetailView
         generic detail view"""
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

    def test_user_dont_see_same_things_if_not_login(self):
        """Test user can't access to some informations
        if not suscribed to community"""
        group = Group.objects.get(name="La communauté de l'anneau")

        response = self.client.get(
            reverse("group:community", args=[group.pk])
        )
        self.assertRaises(KeyError)

    def test_login_user_dont_see_same_things_if_not_group_member(self):
        """Test user can't access to some informations
        if not suscribed to community"""
        user = User.objects.get(username='Sam')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")

        group_member_list = list()
        group_member = GroupMember.objects.filter(user=user)

        # Add communities in which user has suscribed in a list
        # that added to context to verify if user is in a displayed
        # community
        for community_inscription in group_member:
            group_member_list.append(community_inscription.group.name)

        response = self.client.get(
            reverse("group:community", args=[group.pk])
        )
        self.assertEqual(group_member_list, response.context['group_member_list'])

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by CommunityDetailView
        generic detail view's name"""
        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")

        response = self.client.get(
            reverse('group:community', args=[group.pk])
        )
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test CommunityDetailView use the correct template"""
        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")

        response = self.client.get(
            reverse('group:community', args=[group.pk])
        )

        self.assertTemplateUsed(response, 'group/group_detail.html')

    def test_decision_object_is_create_or_get_for_group_member(self):
        """Test decision object is create or get for each
        group member in each call of CommunityDetailView"""
        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=user, group=group)

        decision = Decision.objects.create(
            group=group,
            group_member=group_member,
        )

        response = self.client.get(
            reverse('group:community', args=[group.pk])
        )

        self.assertEqual(
            response.context['delete_group_vote'],
            decision.delete_group_vote
        )

        self.assertEqual(
            response.context['modify_group_vote'],
            decision.modify_group_vote
        )


class GroupInscriptionViewTest(TestCase):
    """Tests on GroupInscriptionView generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupInscriptionView generic view"""
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
        """Test user can't access to GroupInscriptionView generic view
         and it is redirect to login form"""
        response = self.client.get(
            reverse('group:group_inscription')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("group:group_inscription")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        GroupInscriptionView generic view's name"""
        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=user)

        get_response = self.client.get(
            reverse('group:group_inscription'),
        )

        post_response = self.client.post(
            reverse('group:group_inscription'),
            data={
                    'csrfmiddlewaretoken':
                        ['eU8bKFfWaGjL6hNrogiml87GzqsxvzjR'
                         'gDWyJ2px8Yv30cwy0gkCpQWeFNDiIM8S'],
                     'name': ['Comté'],
                     'image': [''],
                     'street': ['2 chemin vert'],
                     'city': ['Saquet'],
                     'postal_code': ['02540'],
                     'country': ['Terre du milieu'],
                 }
        )

        # Check that we got a response "success"
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupInscriptionView generic view
        verify datas correctly"""
        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=self.user)
        true_request = {
                    'csrfmiddlewaretoken':
                        ['eU8bKFfWaGjL6hNrogiml87GzqsxvzjR'
                         'gDWyJ2px8Yv30cwy0gkCpQWeFNDiIM8S'],
                     'name': ['Comté'],
                     'image': [''],
                     'street': ['2 chemin vert'],
                     'city': ['Saquet'],
                     'postal_code': ['02540'],
                     'country': ['Terre du milieu'],
                 }
        true_response = self.client.post(
            reverse('group:group_inscription'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('index')
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('group:group_inscription'),
            data=false_request
        )

        self.assertEqual(
            false_response.status_code,
            200
        )
