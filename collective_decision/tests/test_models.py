"""Tests of collective_decision django models"""

from django.test import TestCase
from django.db import IntegrityError

from ..models import *
from user.models import User
from group.models import Group
from group_member.models import GroupMember
from product.models import Product


class EstimationModelTest(TestCase):
    """Tests on Estimation object"""
    @classmethod
    def setUp(cls):
        """Set up a context to test Estimation object"""
        user = User.objects.create_user(username='Frodon', email='frodon@gmail.com', password='sam')
        group = Group.objects.create(name="La communauté de l'anneau ")

        cls.group_member = GroupMember.objects.create(user=user, group=group)

        cls.product = Product.objects.create(
            name='PS5',
            group=group
        )

        cls.estimation = Estimation.objects.create(
            cost=3,
            group_member=cls.group_member,
            product=cls.product
        )

    def test_estimation_has_group_member(self):
        """Test Estimation object has relation
        with GroupMember object"""
        user = User.objects.get(username='Frodon')
        estimation_group_member = Estimation.objects.get(
            group_member=GroupMember.objects.get(
                user=user
            )
        )
        self.assertEqual(self.estimation, estimation_group_member)

    def test_estimation_has_product(self):
        """Test Estimation object has relation
        with Product object"""
        product = Product.objects.get(name='PS5')
        estimation_product = Estimation.objects.get(product=product)
        self.assertEqual(self.estimation, estimation_product)

    def test_delete_estimation_not_delete_group_member_and_product(self):
        """Test if Estimation object is deleted, GroupMember and Product
        objects are not deleted"""
        estimation = self.estimation
        estimation.delete()
        group_member = self.group_member
        product = self.product

        self.assertTrue(group_member)
        self.assertTrue(product)

    def test_constraints_one_estimation_per_product_and_group_member(self):
        """Test if constraint of one Estimation object between product and group_member is respected"""
        try:
            estimation_two = Estimation.objects.create(
                cost=6,
                group_member=self.group_member,
                product=self.product
            )
            estimation_two.save()
        except IntegrityError:
            estimation_two = 'IntegrityError'

        self.assertEqual(estimation_two, 'IntegrityError')


class DecisionModelTest(TestCase):
    """Tests on Decision object"""
    @classmethod
    def setUp(cls):
        """Set up a context to test Decision object"""
        user = User.objects.create_user(username='Frodon', email='frodon@gmail.com', password='sam')
        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.group_member = GroupMember.objects.create(user=user, group=cls.group)

        cls.decision = Decision.objects.create(
            delete_group_vote=True,
            modify_group_vote=False,
            delete_member_vote=True,
            group_member=cls.group_member,
            group=cls.group
        )

    def test_decision_has_group_member(self):
        """Test Decision object has relation
        with GroupMember object"""
        user = User.objects.get(username='Frodon')
        decision_group_member = Decision.objects.get(
            group_member=GroupMember.objects.get(
                user=user
            )
        )
        self.assertEqual(self.decision, decision_group_member)

    def test_decision_has_group(self):
        """Test Decision object has relation
        with Group object"""
        group = Group.objects.get(name="La communauté de l'anneau")
        decision_group = Decision.objects.get(group=group)
        self.assertEqual(self.decision, decision_group)

    def test_delete_decision_not_delete_group_member_and_group(self):
        """Test if Decision object is deleted, GroupMember and Group
        objects are not deleted"""
        decision = self.decision
        decision.delete()
        group_member = self.group_member
        group = self.group

        self.assertTrue(group_member)
        self.assertTrue(group)

    def test_constraints_one_decision_per_group_and_group_member(self):
        """Test if constraint of one Decision object between group and group_member is respected"""
        try:
            decision_two = Decision.objects.create(
                delete_group_vote=True,
                modify_group_vote=True,
                delete_member_vote=True,
                group_member=self.group_member,
                group=self.group
            )
            decision_two.save()
        except IntegrityError:
            decision_two = 'IntegrityError'

        self.assertEqual(decision_two, 'IntegrityError')
