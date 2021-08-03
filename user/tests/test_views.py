"""Tests of user django views"""

from django.test import TestCase
from django.urls import reverse

from group.models import Group
from group_member.models import GroupMember

from ..models import User


class UserDetailViewTest(TestCase):
    """Tests on UserDetailView generic detail view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test UserDetailView
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

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to UserDetailView generic view
         and it is redirect to login form"""
        response = self.client.get(
            reverse('user:account')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("user:account")}'
        )

    def test_view_uses_correct_template(self):
        """Test UserDetailView use the correct template"""

        user = User.objects.get(username='Frodon')
        self.client.force_login(user)

        response = self.client.get(
            reverse('user:account')
        )

        self.assertTemplateUsed(response, 'user/user_account.html')

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by UserDetailView
        generic detail view's name"""
        user = User.objects.get(username='Frodon')
        self.client.force_login(user)

        get_response = self.client.get(
            reverse('user:account')
        )

        post_response = self.client.post(
            reverse('user:account'),
            data={
                'csrfmiddlewaretoken':
                    ['XlB7R5P9ZjOlIHL3HsNfEoXqcDwC3KuFzg'
                     'rRow6qZwGn8EvBlY0W3OllMdNhaKY6'],
                'username': ['sam'],
                'last_name': ['Saquet'],
                'first_name': ['Frodon'],
                'email': ['frodonsam@live.fr'],
                'street': ['2 rue Mordor'],
                'city': ['Comté'],
                'postal_code': ['95130'],
                'country': ['Terre du Milieu']
            }
        )

        # Check that we got a response "success"
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupInscriptionView generic view
        verify datas correctly"""

        user = User.objects.get(username='Frodon')
        self.client.force_login(user)

        true_request = {
            'csrfmiddlewaretoken':
            ['XlB7R5P9ZjOlIHL3HsNfEoXqcDwC3KuFzg'
             'rRow6qZwGn8EvBlY0W3OllMdNhaKY6'],
            'username': ['sam'],
            'last_name': ['Saquet'],
            'first_name': ['Frodon'],
            'email': ['frodonsam@live.fr'],
            'street': ['2 rue Mordor'],
            'city': ['Comté'],
            'postal_code': ['95130'],
            'country': ['Terre du Milieu']
        }

        true_response = self.client.post(
            reverse('user:account'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('user:account')
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
        }
        false_response = self.client.post(
            reverse('user:account'),
            data=false_request
        )

        self.assertEqual(false_response.status_code, 200)
