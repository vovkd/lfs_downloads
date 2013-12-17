#django
from django import forms
from decimal import Decimal


class DonationAdminForm(forms.Form):
    enable = forms.BooleanField('Enable')
    amount = forms.DecimalField(
        min_value=Decimal('1.00'),
    )
    minimum = forms.DecimalField(
        min_value=Decimal('1.00'),
    )
