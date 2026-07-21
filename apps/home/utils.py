from django.core.mail import send_mail
from django.conf import settings
from . import models as home_models
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from datetime import datetime


def send_email_to_user(user, obj):
    subject = 'Thank you for submitting the warranty form'
    message = f' The warranty claim for {obj.customer_name or obj.Last_Name} has been submitted.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, 'mannanmaan1425@gmail.com']
    send_mail(subject, message, email_from, recipient_list)


def export_all_forms(start_date, end_date):
    import csv
    from django.http import HttpResponse

    if start_date and end_date and start_date <= end_date:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_forms.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'job_number', 'tech_name', 'customer_name', 'Last_Name', 'First_Name',
            'warranty_part', 'warranty_type',
            'claim_number', 'claim_submission_date', 'claim_approval_date',
            'amount_paid', 'status',
            'vendor_submission_method', 'vendor_confirmation_number',
            'vendor_submitted_date', 'notes',
        ])
        all_forms = home_models.WarrantyForm.objects.filter(
            created_at__gte=start_date, created_at__lte=end_date
        )
        for form in all_forms:
            writer.writerow([
                form.job_number, form.tech_name, form.customer_name,
                form.Last_Name, form.First_Name,
                form.warranty_part, form.warranty_type,
                form.claim_number, form.claim_submission_date, form.claim_approval_date,
                form.amount_paid, form.status,
                form.vendor_submission_method, form.vendor_confirmation_number,
                form.vendor_submitted_date, form.notes,
            ])
        return response
    return False, "Invalid Date Range"


def calculate_total_amount_of_this_year_forms(user_all_forms):
    current_year = datetime.now().year
    paid_amount = 0
    for form in user_all_forms:
        try:
            if form.claim_approval_date and form.claim_approval_date.year == current_year:
                paid_amount += (form.amount_paid or 0)
        except Exception:
            pass
    return {
        "paid_amount": f'${paid_amount}',
        "total_forms": user_all_forms.count(),
    }


def calculate_monthly_amount_of_this_year_forms(forms):
    current_year = datetime.now().year
    monthly_amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    monthly_amounts = (
        forms.filter(claim_submission_date__year=current_year)
        .annotate(month=ExtractMonth('claim_submission_date'))
        .values('month')
        .annotate(total_amount=Sum('amount_paid'))
        .order_by('month')
    )
    for amount in monthly_amounts:
        monthly_amount[amount['month'] - 1] = int(amount['total_amount']) if amount['total_amount'] else 0
    return monthly_amount


def calculate_monthly_quantity_of_this_year_forms(forms):
    current_year = datetime.now().year
    monthly_quantity = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    monthly_quantities = (
        forms.filter(claim_submission_date__year=current_year)
        .annotate(month=ExtractMonth('claim_submission_date'))
        .values('month')
        .annotate(form_count=Count('id'))
        .order_by('month')
    )
    for quantity in monthly_quantities:
        monthly_quantity[quantity['month'] - 1] = quantity['form_count']
    return monthly_quantity
