"""Manage product app forms"""

from django import forms
from collective_decision.models import Estimation

from .models import Product


class ProductInscriptionForm(forms.ModelForm):
    """ Sign in forms to permit the users to modify him"""
    group_member = forms.BooleanField()
    community = forms.BooleanField()

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'image',
            'user_provider', 'group_provider',
            'group', 'estimator']


class CostEstimationForm(forms.ModelForm):

    class Meta:
        model = Estimation
        fields = ['cost']
