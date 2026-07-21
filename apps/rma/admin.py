from django.contrib import admin
from .models import PartsReturn


@admin.register(PartsReturn)
class PartsReturnAdmin(admin.ModelAdmin):
    list_display = ['rma_number', 'client_name', 'order_number', 'date_rma_requested', 'date_rma_credit_received', 'created_at']
    search_fields = ['rma_number', 'client_name', 'order_number']
    list_filter = ['date_rma_requested', 'date_rma_credit_received']
