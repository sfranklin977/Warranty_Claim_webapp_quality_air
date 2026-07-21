# -*- encoding: utf-8 -*-
"""Copyright (c) 2019 - present AppSeed.us"""
from django.contrib import admin
from . import models as home_models
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class WarrantyFormResource(resources.ModelResource):
    class Meta:
        model = home_models.WarrantyForm
        fields = (
            'id', 'job_number', 'tech_name',
            'customer_name', 'Last_Name', 'First_Name',
            'warranty_part', 'warranty_type',
            'claim_number', 'claim_submission_date', 'claim_approval_date',
            'amount_paid', 'status',
            'vendor_submission_method', 'vendor_confirmation_number',
            'vendor_submitted_date',
            'notes',
        )


@admin.register(home_models.WarrantyForm)
class WarrantyFormAdmin(ImportExportModelAdmin):
    resource_class = WarrantyFormResource
    list_display = [
        'claim_number', 'job_number', 'customer_name', 'warranty_part',
        'warranty_type', 'status', 'amount_paid', 'created_at',
    ]
    list_filter = ['warranty_type', 'status', 'vendor_submission_method']
    search_fields = ['claim_number', 'job_number', 'customer_name', 'Last_Name', 'First_Name', 'warranty_part']
