"""Manage group app forms"""

from django import forms

from product.models import Product
from geolocalisation.models import Address
from collective_decision.models import Estimation

from .models import Group


class GroupInscriptionForm(forms.ModelForm):
    """ModelForm to create a group"""

    class Meta:
        model = Group
        fields = [
            'name', 'address', 'image',
            'url', 'private'
        ]


class ProductInscriptionForm(forms.ModelForm):
    """ModelForm to create a product"""

    group_member = forms.BooleanField()
    community = forms.BooleanField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'image']


class CostEstimationForm(forms.ModelForm):
    """ModelForm to create a product cost estimation"""

    class Meta:
        model = Estimation
        fields = ['cost']


class AddressForm(forms.ModelForm):
    """ModelForm to create a postal address"""

    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code', 'country']
