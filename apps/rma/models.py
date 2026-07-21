from django.db import models
from django.contrib.auth.models import User


class PartsReturn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    client_name = models.CharField(max_length=200)
    order_number = models.CharField(max_length=100)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    model_number = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    rma_number = models.CharField(max_length=100)
    date_rma_requested = models.DateField(null=True, blank=True)
    date_rma_credit_received = models.DateField(null=True, blank=True)
    rma_credit_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    replacement_ordered_date = models.DateField(null=True, blank=True)
    replacement_order_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RMA {self.rma_number} — {self.client_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Parts Return"
        verbose_name_plural = "Parts Returns"
