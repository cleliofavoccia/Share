"""Manage collective_decision app forms"""

from django import forms

from group.models import Group
from group_member.models import GroupMember

from .models import Decision


class GroupMemberVoteForm(forms.Form):
    """Form to manage GroupMembers votes objects
    about Group modification"""
    group_member = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    group = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    def clean_group_member(self):
        """Return the GroupMember object since the id input
        by user, if it exists"""
        group_member_id = self.cleaned_data['group_member']
        try:
            group_member = GroupMember.objects.get(id=group_member_id)
        except GroupMember.DoesNotExist:
            raise forms.ValidationError("Ce membre du groupe n'existe pas !")

        return group_member

    def clean_group(self):
        """Return the Group object
        since the id input by user, if it exists"""
        group_id = self.cleaned_data['group']
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise forms.ValidationError("Cette communauté n'existe pas !")

        return group

    def save_delete_group_vote(self, commit=True):
        """Save the GroupMember delete vote community
        build with his inputs"""
        group_member = self.cleaned_data['group_member']
        group = self.cleaned_data['group']
        try:
            decision = Decision.objects.get(group_member=group_member,
                                            group=group)

            if commit:
                decision.delete()

                decision = Decision(
                    group_member=group_member, group=group,
                    delete_group_vote=True
                )
                decision.save()

        except Decision.DoesNotExist:
            decision = Decision(
                group_member=group_member, group=group,
                delete_group_vote=True
            )

            if commit:
                decision.save()

        return decision

    def save_against_delete_group_vote(self, commit=True):
        """Save the GroupMember against delete vote community
        build with his inputs"""
        group_member = self.cleaned_data['group_member']
        group = self.cleaned_data['group']
        try:
            decision = Decision.objects.get(group_member=group_member,
                                            group=group)

            if commit:
                decision.delete()

                decision = Decision(
                    group_member=group_member, group=group,
                    delete_group_vote=False
                )
                decision.save()

        except Decision.DoesNotExist:
            decision = Decision(
                group_member=group_member, group=group,
                delete_group_vote=False
            )

            if commit:
                decision.save()

        return decision

    def save_modify_group_vote(self, commit=True):
        """Save the GroupMember modify vote community
        build with his inputs"""
        group_member = self.cleaned_data['group_member']
        group = self.cleaned_data['group']
        try:
            decision = Decision.objects.get(group_member=group_member,
                                            group=group)

            if commit:
                decision.delete()

                decision = Decision(
                    group_member=group_member, group=group,
                    modify_group_vote=True
                )
                decision.save()

        except Decision.DoesNotExist:
            decision = Decision(
                group_member=group_member, group=group,
                modify_group_vote=True
            )

            if commit:
                decision.save()

        return decision

    def save_against_modify_group_vote(self, commit=True):
        """Save the GroupMember against modify vote community
        build with his inputs"""
        group_member = self.cleaned_data['group_member']
        group = self.cleaned_data['group']
        try:
            decision = Decision.objects.get(group_member=group_member,
                                            group=group)

            if commit:
                decision.delete()

                decision = Decision(
                    group_member=group_member, group=group,
                    modify_group_vote=False
                )
                decision.save()

        except Decision.DoesNotExist:
            decision = Decision(
                group_member=group_member, group=group,
                modify_group_vote=False
            )

            if commit:
                decision.save()

        return decision
