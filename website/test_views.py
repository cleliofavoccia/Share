"""Tests of website django views"""

from django.test import TestCase
from django.urls import reverse

from user.models import User


class FailViewTest(TestCase):
    """Test FailView generic View"""
    @classmethod
    def setUp(cls):
        """Set up a context to test FailView generic view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to FailView generic view
        and it is redirect to login form"""
        response = self.client.get(reverse('website:fail'))
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("website:fail")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by FailView generic view's name"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('website:fail'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(response.context['user'].username, 'Frodon')

    def test_view_fail_message(self):
        """Test view display the desired message"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('website:fail'))

        self.assertEqual(
            response.context['msg_fail'],
            "Oups ! Il a dû se produire une erreur. Réessayer ou bien,"
            "en cas de persistence du problème, contactez l'administration"
            "du site"
        )

    def test_view_uses_correct_template(self):
        """Test FailView use the correct template"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('website:fail'))

        self.assertTemplateUsed(response, 'website/fail.html')
