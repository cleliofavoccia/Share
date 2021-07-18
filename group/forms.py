
from product.models import Product
from .models import Group
from geolocalisation.models import Address
from collective_decision.models import Estimation
from django import forms


class GroupInscriptionForm(forms.ModelForm):
    """ Sign in forms to permit the users to modify him"""

    class Meta:
        model = Group
        fields = ['name', 'address', 'image']


class ProductInscriptionForm(forms.ModelForm):
    """ Sign in forms to permit the users to modify him"""
    group_member = forms.BooleanField()
    community = forms.BooleanField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'image']


class CostEstimationForm(forms.ModelForm):

    class Meta:
        model = Estimation
        fields = ['cost']


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code', 'country']
