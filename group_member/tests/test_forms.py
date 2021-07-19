"""Tests of group_member django forms"""

from django.test import TestCase

from user.models import User
from group.models import Group

from ..models import GroupMember
from ..forms import GroupMemberInscriptionForm


class GroupMemberInscriptionFormTest(TestCase):
    """Tests on GroupMemberInscriptionForm"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberInscriptionForm object"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.cleaned_data = {
            'group_member': None,
            'group': None
        }

    def test_form_work_with_existant_datas(self):
        """Test GroupMemberInscriptionForm work with existant User,
        and Group instance"""
        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")

        form = GroupMemberInscriptionForm(data={
            'user': user.id,
            'group': group.id,
        })
        self.assertTrue(form.is_valid())

    def test_form_doesnt_work_with_unexistant_datas(self):
        """Test GroupMemberInscriptionForm doesn't work with unexistant datas
        or existant and unexistant datas. Datas are User and
        Group instance"""
        user = User.objects.get(username='Frodon')
        try:
            group = Group.objects.get(name="Mordor")
        except Group.DoesNotExist:
            group = {'name': 'Mordor', 'id': '1'}

        form = GroupMemberInscriptionForm(data={
            'user': user.id,
            'group': group['id']
        })
        self.assertFalse(form.is_valid())

        try:
            user = User.objects.get(username='Sam')
        except User.DoesNotExist:
            user = {'name': 'Sam', 'id': '1'}
        try:
            group = Group.objects.get(name="Mordor")
        except Group.DoesNotExist:
            group = {'name': 'Mordor', 'id': '1'}
        form = GroupMemberInscriptionForm(data={
            'user': user['id'],
            'group': group['id']
        })
        self.assertFalse(form.is_valid())

        try:
            user = User.objects.get(username='Sam')
        except User.DoesNotExist:
            user = {'name': 'Sam', 'id': '1'}
        group = Group.objects.get(name="La communauté de l'anneau")
        form = GroupMemberInscriptionForm(data={
            'user': user['id'],
            'group': group.id
        })
        self.assertFalse(form.is_valid())

    def test_form_save_group_member_objects(self):
        """Test GroupMemberInscriptionForm return
        and save GroupMember object"""
        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        group = Group.objects.get(name="La communauté de l'anneau")
        data = {
            'user': user.id,
            'group': group.id
        }
        form = GroupMemberInscriptionForm(data=data)
        form.is_valid()

        new_group_member = form.save(user)
        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )

        self.assertEqual(new_group_member, group_member)

    def test_form_delete_group_member_objects(self):
        """Test GroupMemberInscriptionForm return and
        delete GroupMember object"""
        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        group = Group.objects.get(name="La communauté de l'anneau")
        data = {
            'user': user.id,
            'group': group.id
        }
        form = GroupMemberInscriptionForm(data=data)
        form.is_valid()

        form.delete(user)
        try:
            group_member = GroupMember.objects.get(
                user=user,
                group=group
            )
        except GroupMember.DoesNotExist:
            group_member = 'DoesNotExist'

        self.assertEqual(group_member, 'DoesNotExist')

    def test_clean_user(self):
        """Test GroupMemberInscriptionForm verify if User
        input by user exist and is valid"""
        user = User.objects.get(username='Frodon')
        self.cleaned_data['user'] = user.id
        self.assertEqual(
            user,
            GroupMemberInscriptionForm.clean_user(self)
        )

    def test_clean_group(self):
        """Test GroupMemberVoteForm verify if Group
        input by user exist and is valid"""
        group = Group.objects.get(name="La communauté de l'anneau")
        self.cleaned_data['group'] = group.id
        self.assertEqual(group, GroupMemberInscriptionForm.clean_group(self))
