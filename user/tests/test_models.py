"""Tests of user django models"""

from django.test import TestCase
from django.db import IntegrityError

from geolocalisation.models import Address

from ..models import User


class UserModelTest(TestCase):
    """Tests on User object"""
    @classmethod
    def setUp(cls):
        """Set up a context to test User object"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

        cls.address = Address.objects.create(
            street='2 rue Isildur',
            city='Minas Tirith',
            postal_code='80000',
            country='Terre du Milieu'
        )

    def test_user_has_address(self):
        """Test User object has relation
        with Address object"""

        user = User.objects.get(username='Frodon')
        address = Address.objects.get(street='2 rue Isildur')

        user.address = address

        self.assertEqual(user.address, address)

    def test_delete_user_not_delete_address(self):
        """Test if User object is deleted, Address
        object is not deleted"""

        user = User.objects.get(username='Frodon')
        address = Address.objects.get(street='2 rue Isildur')

        user.address = address

        address.delete()

        self.assertTrue(user)

    def test_constraints_one_email_per_user(self):
        """Test if email is unique for User object"""

        try:
            user_2 = User.objects.create_user(
                username='Sam',
                email='frodon@gmail.com',
                password='frodon'
            )
        except IntegrityError:
            user_2 = 'IntegrityError'

        self.assertEqual(user_2, 'IntegrityError')

    def test_username_are_not_unique(self):
        """Test if user is not unique for User object"""

        try:
            user_2 = User.objects.create_user(
                username='Frodon',
                email='sam@gmail.com',
                password='frodon'
            )
        except IntegrityError:
            user_2 = 'IntegrityError'

        self.assertTrue(user_2)
