"""Manage forms of dashboard app"""

from django import forms


class CommunityResearchForm(forms.Form):
    """Form that send a community name to find a
    community of the same name"""

    research = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Recherche une communauté'
            }
        )
    )
