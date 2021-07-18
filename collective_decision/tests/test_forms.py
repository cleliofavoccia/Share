"""Tests of collective_decision django forms"""
from django.test import TestCase

from user.models import User
from ..forms import GroupMemberVoteForm

from collective_decision.models import Decision
from group.models import Group
from group_member.models import GroupMember


class GroupMemberVoteFormTest(TestCase):
    """Tests on GroupMemberVoteForm"""
    @classmethod
    def setUp(cls):
        """Set up a context to test GroupMemberVoteForm object"""
        cls.user = User.objects.create_user(username='Frodon', email='frodon@gmail.com', password='sam')
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(user=cls.user, group=cls.group)

        cls.cleaned_data = {
            'group_member': None,
            'group': None
        }

    def test_group_member_vote_form_work_with_existant_datas(self):
        """Test GroupMemberVoteForm work with existant User,
        GroupMember and Group instance"""
        user = User.objects.get(username='Frodon')
        group_member = GroupMember.objects.get(user=user)
        group = Group.objects.get(name="La communauté de l'anneau")

        form = GroupMemberVoteForm(data={
            'group_member': group_member.id,
            'group': group.id,
        })
        self.assertTrue(form.is_valid())

    def test_group_member_vote_form_doesnt_work_with_unexistant_datas(self):
        """Test GroupMemberVoteForm doesn't work with unexistant datas
        or existant and unexistant datas. Datas are User, GroupMember and
        Group instance"""
        user = User.objects.get(username='Frodon')
        group_member = GroupMember.objects.get(user=user)
        try:
            group = Group.objects.get(name="Mordor")
        except Group.DoesNotExist:
            group = {'name': 'Mordor', 'id' : '1'}

        form = GroupMemberVoteForm(data={
            'group_member': group_member.id,
            'group': group['id']
        })
        self.assertFalse(form.is_valid())

        try:
            user = User.objects.get(username='Sam')
        except User.DoesNotExist:
            user = {'name': 'Sam', 'id' : '1'}
        try:
            group_member = GroupMember.objects.get(user=user['id'])
        except GroupMember.DoesNotExist:
            group_member = {'name': 'Sam', 'id' : '1'}
        try:
            group = Group.objects.get(name="Mordor")
        except Group.DoesNotExist:
            group = {'name': 'Mordor', 'id': '1'}
        form = GroupMemberVoteForm(data={
            'group_member': group_member['id'],
            'group': group['id']
        })
        self.assertFalse(form.is_valid())

        try:
            user = User.objects.get(username='Sam')
        except User.DoesNotExist:
            user = {'name': 'Sam', 'id': '1'}
        try:
            group_member = GroupMember.objects.get(user=user['id'])
        except GroupMember.DoesNotExist:
            group_member = {'name': 'Sam', 'id': '1'}
        group = Group.objects.get(name="La communauté de l'anneau")
        form = GroupMemberVoteForm(data={
            'group_member': group_member['id'],
            'group': group.id
        })
        self.assertFalse(form.is_valid())

    def test_group_member_vote_form_save_decision_objects(self):
        """Test GroupMemberVoteForm return and save Decision object"""
        self.client.force_login(self.user)

        user = User.objects.get(username='Frodon')
        group_member = GroupMember.objects.get(user=user)
        group = Group.objects.get(name="La communauté de l'anneau")
        data = {
            'group_member': group_member.id,
            'group': group.id
        }
        form = GroupMemberVoteForm(data=data)
        form.is_valid()

        delete_vote = form.save_delete_group_vote(self.user)
        decision_1 = Decision.objects.get(group_member=group_member,
                                          group=group)
        against_delete_vote = form.save_against_delete_group_vote(self.user)
        decision_2 = Decision.objects.get(group_member=group_member,
                                          group=group)
        modify_vote = form.save_modify_group_vote(self.user)
        decision_3 = Decision.objects.get(group_member=group_member,
                                          group=group)
        against_modify_vote = form.save_against_modify_group_vote(self.user)
        decision_4 = Decision.objects.get(group_member=group_member,
                                          group=group)

        self.assertEqual(delete_vote, decision_1)
        self.assertEqual(against_delete_vote, decision_2)
        self.assertEqual(modify_vote, decision_3)
        self.assertEqual(against_modify_vote, decision_4)

    def test_clean_group_member(self):
        """Test GroupMemberVoteForm verify if GroupMember
        input by user exist and is valid"""
        user = User.objects.get(username='Frodon')
        group_member = GroupMember.objects.get(user=user)
        self.cleaned_data['group_member'] = group_member.id
        self.assertEqual(group_member, GroupMemberVoteForm.clean_group_member(self))

    def test_clean_group(self):
        """Test GroupMemberVoteForm verify if Group
        input by user exist and is valid"""
        group = Group.objects.get(name="La communauté de l'anneau")
        self.cleaned_data['group'] = group.id
        self.assertEqual(group, GroupMemberVoteForm.clean_group(self))
