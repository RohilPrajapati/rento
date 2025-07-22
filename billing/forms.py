from django import forms
from billing.models import Rentee, ElectricityBill
from nepali_datetime_field.forms import NepaliDateField

class RenteeForm(forms.ModelForm):
    class Meta:
        model = Rentee
        fields = ['full_name', 'email']

class ElectricityBillForm(forms.ModelForm):
    billing_month = NepaliDateField()

    class Meta:
        model = ElectricityBill
        fields = [
            'rentee', 'billing_month', 'previous_reading', 'current_reading',
            'rate_per_unit', 'bill_status'
        ]

    def clean_billing_month(self):
        value = self.cleaned_data['billing_month']
        return value.replace(day=1)  # Normalize to the first day of the month