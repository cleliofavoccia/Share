"""Tests of group_member django models"""

from django.test import TestCase

from user.models import User
from group.models import Group

from ..models import GroupMember


class GroupMemberModelTest(TestCase):
    """Tests on Group object"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMember object"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

        cls.group = Group.objects.create(
            name="La communauté de l'anneau"
        )

        cls.group_member = GroupMember.objects.create(
            user=cls.user, group=cls.group
        )

    def test_group_member_has_user(self):
        """Test GroupMember object has relation
        with User object"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )
        self.assertEqual(group_member.user, user)

    def test_group_member_has_group(self):
        """Test GroupMember object has relation
        with Group object"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )
        self.assertEqual(group_member.group, group)

    def test_delete_group_member_not_delete_user_and_group(self):
        """Test if Group object is deleted, User
        objects are not deleted"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )
        group_member.delete()

        self.assertTrue(user)
        self.assertTrue(group)
