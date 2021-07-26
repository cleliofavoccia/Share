"""Manage group_member app forms"""

from django import forms

from group.models import Group
from user.models import User
from product.models import Product

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


class GroupMemberRentalForm(forms.Form):
    """Form to to permit community member
    (GroupMember objects),
    to rent products (Product object)"""

    product = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    group_member = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    def clean_product(self):
        """Return the Product object since the id input
        by user, if it exists"""
        product_id = self.cleaned_data['product']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise forms.ValidationError("Ce produit n'existe pas !")

        return product

    def clean_group_member(self):
        """Return the GroupMember object
        since the id input by user, if it exists"""
        group_member_id = self.cleaned_data['group_member']
        try:
            group_member = GroupMember.objects.get(id=group_member_id)
        except GroupMember.DoesNotExist:
            raise forms.ValidationError("Ce membre de la communauté n'existe pas !")

        return group_member

    def save(self, commit=True):
        """Save the Product object modification build by
        user's profil and the product input by user"""

        product = self.cleaned_data['product']
        group_member = self.cleaned_data['group_member']

        product.tenant = group_member

        if commit:
            product.save()
        return product

    def delete(self, commit=True):
        """Delete the Product object modification request by user"""

        product = self.cleaned_data['product']
        group_member = self.cleaned_data['group_member']

        product.tenant = None

        if commit:
            product.save()
        return product
