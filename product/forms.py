
from .models import Product
from collective_decision.models import Estimation
from django import forms


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
