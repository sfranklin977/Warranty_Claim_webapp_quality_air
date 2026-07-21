from django import forms
from . import models as home_models


class WarrantyForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}), required=False
    )
    claim_submission_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=False
    )
    claim_approval_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=False
    )
    vendor_submitted_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=False
    )

    class Meta:
        model = home_models.WarrantyForm
        fields = [
            'job_number', 'tech_name',
            'customer_name', 'Last_Name', 'First_Name',
            'warranty_part', 'warranty_type',
            'claim_number', 'claim_submission_date', 'claim_approval_date',
            'amount_paid', 'status',
            'vendor_submission_method', 'vendor_confirmation_number',
            'vendor_submitted_date',
            'notes', 'invoice_file',
        ]
