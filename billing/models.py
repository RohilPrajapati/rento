from django.db import models
from django.core.exceptions import ValidationError
from nepali_datetime_field.models import NepaliDateField

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
        return  f"{self.full_name} ({self.email})"

class ElectricityBill(models.Model):
    BILL_STATUS_CHOICES = (
        ('paid','Paid'),
        ('pending','Pending')
    )
    rentee = models.ForeignKey(Rentee, on_delete=models.PROTECT)
    billing_month = NepaliDateField()
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2)
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)
    units_consumed = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    rate_per_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bill_status = models.CharField(choices=BILL_STATUS_CHOICES, default='pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-billing_month']
        unique_together = ['rentee', 'billing_month']

    def save(self, *args, **kwargs):
        self.units_consumed = self.current_reading - self.previous_reading
        self.total_amount = self.units_consumed * self.rate_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rentee.full_name} - {self.billing_month.strftime('%B %Y')}"
