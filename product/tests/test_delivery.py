"""Tests of delivery django commands"""

import datetime

from django.test import TestCase
from django.utils.timezone import make_aware

from user.models import User
from group.models import Group
from group_member.models import GroupMember

from ..models import Product


class DeliveryCommandTest(TestCase):
    """Tests on DeliveryCommand"""
    @classmethod
    def setUp(cls):
        """Set up a context to test DeliveryCommand object"""
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

        cls.rental_end = datetime.datetime(2021, 8, 21)

        cls.product = Product.objects.create(
            name='Epée',
            group=cls.group,
            user_provider=cls.group_member,
            tenant=cls.group_member,
            rental_end=cls.rental_end
        )

    def test_verify_datetime_objects_work(self):
        """Test verify datetime objects work
        correctly and delivery command work
        with. Verify if in this case,
        conscient and naive datetime don't
        disturb the process."""

        product = Product.objects.get(name='Epée')
        today = make_aware(self.rental_end)

        group_member = GroupMember.objects.get(
            user=product.tenant.user,
            group=product.tenant.group
        )

        group_member.points_penalty -= 1

        group_member.save()

        if product.rental_end.day == today.day:
            group_member.points_penalty = 0

            group_member.save()

            product.tenant = None
            product.delivered = False

            product.save()

        self.assertFalse(product.delivered)
        self.assertIsNone(product.tenant)
