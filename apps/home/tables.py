import django_tables2 as tables
from django.utils.html import format_html
from . import models as home_models


class WarrantyFormTable(tables.Table):
    invoice_file = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {
            "class": 'table table-sm table-stripped data-table',
            'data-add-url': 'Url here'
        }
        model = home_models.WarrantyForm
        fields = [
            'job_number',
            'tech_name',
            'customer_name',
            'Last_Name',
            'First_Name',
            'warranty_part',
            'warranty_type',
            'claim_number',
            'claim_submission_date',
            'claim_approval_date',
            'amount_paid',
            'status',
            'vendor_submission_method',
            'vendor_confirmation_number',
            'vendor_submitted_date',
            'notes',
            'invoice_file',
        ]

    def render_invoice_file(self, record):
        try:
            if record.invoice_file:
                return format_html('<a href="{}" target="_blank">View Invoice</a>', record.invoice_file.url)
        except Exception:
            pass
        return ""
