"""Tests of group django models"""

from django.test import TestCase

from user.models import User
from group_member.models import GroupMember
from geolocalisation.models import Address
from collective_decision.models import Decision

from ..models import Group


class GroupModelTest(TestCase):
    """Tests on Group object"""
    @classmethod
    def setUp(cls):
        """Set up a context to test Group object"""
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
            user=cls.user1, group=cls.group
        )

    def test_group_has_group_members(self):
        """Test Group object has relation
        with GroupMember object"""
        user = User.objects.get(username='Sam')
        group = Group.objects.get(name="La communauté de l'anneau")

        group_member = GroupMember.objects.create(
            user=user,
            group=group
        )
        self.assertTrue(group_member)

    def test_group_has_address(self):
        """Test Group object has relation
        with Address object"""
        address = Address.objects.get(street='2 rue Isildur')
        group_address = Group.objects.get(address=address)
        self.assertEqual(self.group.address, address)

    def test_group_has_decisions(self):
        """Test Group object has relation
        with Decision object"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(user=user)
        decision = Decision.objects.create(
            group_member=group_member,
            group=group,
        )

        self.assertTrue(decision)

    def test_delete_group_delete_group_member(self):
        """Test if Group object is deleted, GroupMember
        objects are deleted"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        group.delete()
        try:
            group_member = GroupMember.objects.get(user=user)
        except GroupMember.DoesNotExist:
            group_member = 'DoesNotExist'

        self.assertEqual(group_member, 'DoesNotExist')

    def test_delete_group_delete_decisions(self):
        """Test if Group object is deleted, Decision
        objects are deleted"""
        group = Group.objects.get(name="La communauté de l'anneau")
        group.delete()
        try:
            decision = Decision.objects.get(group=group)
        except Decision.DoesNotExist:
            decision = 'DoesNotExist'

        self.assertEqual(decision, 'DoesNotExist')

    def test_delete_group_not_delete_address(self):
        """Test if Group object is deleted, Address
        objects are not deleted"""
        group = Group.objects.get(name="La communauté de l'anneau")
        group.delete()
        address = Address.objects.get(street=group.address.street)

        self.assertTrue(address)
