from django import forms

from billing.models import Rentee, ElectricityBill


class RenteeForm(forms.ModelForm):
    class Meta:
        model = Rentee
        fields = ['full_name', 'email']


class ElectricityBillForm(forms.ModelForm):
    class Meta:
        model = ElectricityBill
        fields = [
            'rentee', 'billing_month', 'billing_year', 'previous_reading', 'current_reading',
            'rate_per_unit', 'bill_status'
        ]
