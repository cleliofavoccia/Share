"""Manage group_member app forms"""

from django import forms

from group.models import Group
from user.models import User

from .models import GroupMember


class GroupMemberInscriptionForm(forms.Form):
    """Form to add GroupMembers objects,
    to user community inscription"""
    user = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    group = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    def clean_user(self):
        """Return the User object since the id input
        by user, if it exists"""
        user_id = self.cleaned_data['user']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas !")

        return user

    def clean_group(self):
        """Return the Group object
        since the id input by user, if it exists"""
        group_id = self.cleaned_data['group']
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise forms.ValidationError("Cette communauté n'existe pas !")

        return group

    def save(self, user, commit=True):
        """Save the object GroupMember build by
        user's profil and the group input by user"""
        user = self.cleaned_data['user']
        group = self.cleaned_data['group']
        group_member = GroupMember(
            user=user, group=group
        )
        if commit:
            group_member.save()
        return group_member

    def delete(self, user, commit=True):
        """Delete the object GroupMember request by user"""
        user = self.cleaned_data['user']
        group = self.cleaned_data['group']
        group_member = GroupMember.objects.filter(
            user=user, group=group
        )
        if group_member and commit:
            group_member.delete()
        return group_member
