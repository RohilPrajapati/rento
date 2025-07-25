import nepali_datetime
from django.core.exceptions import ValidationError
from django.db import models

from elec_proj.constants import DATE_MONTH_CHOICES


class Rentee(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def clean(self):
        if not self.is_deleted:
            existing = Rentee.objects.filter(full_name=self.full_name, is_deleted=False)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError({'full_name': 'A rentee with this name already exists.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # calls clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class ElectricityBill(models.Model):
    BILL_STATUS_CHOICES = (('paid', 'Paid'), ('pending', 'Pending'))
    rentee = models.ForeignKey(Rentee, on_delete=models.PROTECT)
    billing_month = models.PositiveSmallIntegerField(choices=DATE_MONTH_CHOICES)
    billing_year = models.IntegerField(default=nepali_datetime.date.today().year)
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2)
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)
    units_consumed = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    rate_per_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bill_status = models.CharField(choices=BILL_STATUS_CHOICES, default='pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-billing_month', '-billing_year']
        unique_together = ['rentee', 'billing_month', 'billing_year']

    def clean(self):
        super().clean()
        current_date = nepali_datetime.date.today()
        current_month, current_year = current_date.month, current_date.year

        previous = self.previous_reading
        current = self.current_reading
        billing_month = self.billing_month
        billing_year = self.billing_year
        rate = self.rate_per_unit

        errors = {}

        # Validate readings comparison
        if previous is not None and current is not None:
            if previous > current:
                errors['previous_reading'] = 'Previous reading must be less than or equal to current reading.'
                errors['current_reading'] = 'Current reading must be greater than or equal to previous reading.'

        if billing_year is not None and billing_month is not None:
            if billing_year > current_year or (billing_year == current_year and billing_month > current_month):
                errors['billing_month'] = 'Billing date cannot be in the future.'

        if rate is not None and rate <= 0:
            errors['rate_per_unit'] = 'Rate per unit cannot be negative or Zero.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.units_consumed = self.current_reading - self.previous_reading
        self.total_amount = self.units_consumed * self.rate_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rentee.full_name} - {self.get_billing_month_display()} - {self.billing_year}"
