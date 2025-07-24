from django import forms

from billing.models import Rentee, ElectricityBill


class RenteeForm(forms.ModelForm):
    class Meta:
        model = Rentee
        fields = ['full_name', 'email']


class ElectricityBillForm(forms.ModelForm):
    class Meta:
        model = ElectricityBill
        fields = ['rentee', 'billing_month', 'billing_year', 'previous_reading', 'current_reading', 'rate_per_unit',
            'bill_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget,
                          (forms.TextInput, forms.NumberInput, forms.DateInput, forms.EmailInput, forms.Textarea)):
                widget.attrs['class'] = 'form-control'
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
