"""Manage product app forms"""

from django import forms

from collective_decision.models import Estimation
from group.models import Group

from .models import Product


class ProductInscriptionForm(forms.ModelForm):
    """ Sign in forms to permit the users to modify him"""

    group_member = forms.BooleanField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'group_member']


class CostEstimationForm(forms.ModelForm):

    class Meta:
        model = Estimation
        fields = ['cost']


class ProductSuppressionForm(forms.Form):

    product_to_delete = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    group = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )

    def clean_product_to_delete(self):
        """Return the Group object
        since the id input by user, if it exists"""
        product_to_delete_id = self.cleaned_data['product_to_delete']
        try:
            product_to_delete = Product.objects.get(id=product_to_delete_id)
        except Product.DoesNotExist:
            raise forms.ValidationError("Ce produit n'existe pas !")

        return product_to_delete

    def clean_group(self):
        """Return the Group object
        since the id input by user, if it exists"""
        group_id = self.cleaned_data['group']
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            raise forms.ValidationError("Ce produit n'existe pas !")

        return group

    def delete(self, commit=True):
        """Delete the object GroupMember request by user"""

        product = self.cleaned_data['product_to_delete']

        if product and commit and not product.tenant:
            product.delete()
            return 'OK'
        return 'NOT'
