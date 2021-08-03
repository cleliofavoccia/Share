"""Tests of product django models"""

from django.test import TestCase

from user.models import User
from group.models import Group
from group_member.models import GroupMember
from geolocalisation.models import Address
from collective_decision.models import Estimation

from ..models import Product


class ProductModelTest(TestCase):
    """Tests on Product object"""
    @classmethod
    def setUp(cls):
        """Set up a context to test Product object"""
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

        cls.group = Group.objects.create(
            name="La communauté de l'anneau",
            address=cls.address,
        )

        cls.group_member = GroupMember.objects.create(
            user=cls.user, group=cls.group
        )

        cls.product1 = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            tenant=cls.group_member,
            group=cls.group,
        )

        cls.product2 = Product.objects.create(
            name='Dague',
            group_provider=cls.group,
            tenant=cls.group_member,
            group=cls.group,
        )

        cls.estimation1 = Estimation(
            cost=20,
            group_member=cls.group_member,
            product=cls.product1
        )

        cls.estimation2 = Estimation(
            cost=20,
            group_member=cls.group_member,
            product=cls.product2
        )

    def test_product_has_user_provider(self):
        """Test Product object has relation
        with GroupMember object"""

        product = Product.objects.get(name='Epée')

        self.assertTrue(product.user_provider)

    def test_product_has_group_provider(self):
        """Test Product object has relation
        with Group object"""

        product = Product.objects.get(name='Dague')

        self.assertTrue(product.group_provider)

    def test_product_has_tenant(self):
        """Test Product object has an other
        relation with GroupMember object"""

        product = Product.objects.get(name='Dague')

        self.assertTrue(product.tenant)

    def test_product_has_group(self):
        """Test Product object has an other
        relation with Group object"""

        product = Product.objects.get(name='Epée')

        self.assertTrue(product.group)

    def test_product_has_estimation(self):
        """Test Product object has relation
        with Estimation object"""

        product = Product.objects.get(name='Epée')

        self.assertTrue(product.estimator)

    def test_delete_product_not_delete_group_member(self):
        """Test if Product object is deleted, GroupMember
        objects are deleted"""
        user = User.objects.get(username='Frodon')
        product = Product.objects.get(name="Epée")
        product.delete()

        group_member = GroupMember.objects.get(user=user)

        self.assertTrue(group_member)

    def test_delete_product_not_delete_group(self):
        """Test if Product object is deleted, Group
        objects are deleted"""
        product = Product.objects.get(name="Dague")
        product.delete()

        group = Group.objects.get(name="La communauté de l'anneau")

        self.assertTrue(group)

    def test_delete_product_delete_estimation(self):
        """Test if Product object is deleted, Group
        objects are deleted"""
        user = User.objects.get(username='Frodon')
        product = Product.objects.get(name="Epée")
        product.delete()

        group_member = GroupMember.objects.get(user=user)

        try:
            estimation = Estimation.objects.get(
                cost='20',
                group_member=group_member,
                product=product
            )
        except Estimation.DoesNotExist:
            estimation = 'DoesNotExist'

        self.assertEqual(estimation, 'DoesNotExist')
