from django import forms
from billing.models import Rentee, ElectricityBill

class RenteeForm(forms.ModelForm):
    class Meta:
        model = Rentee
        fields = ['full_name', 'email']

class ElectricityBillForm(forms.ModelForm):
    billing_month = forms.DateField(
        input_formats=['%Y-%m'],
        widget=forms.TextInput(attrs={'type': 'month'}),
        help_text="Select the billing month (use first day of month)"
    )

    class Meta:
        model = ElectricityBill
        fields = [
            'rentee', 'billing_month', 'previous_reading', 'current_reading',
            'rate_per_unit', 'bill_status'
        ]

    def clean_billing_month(self):
        value = self.cleaned_data['billing_month']
        return value.replace(day=1)  # Normalize to the first day of the month