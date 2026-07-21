# -*- encoding: utf-8 -*-
"""Copyright (c) 2019 - present AppSeed.us"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from . import models as home_models
from . import tables as home_tables
from . import forms as home_forms
from . import utils as home_utils


@login_required(login_url="/login/")
def index(request):
    user_all_forms = home_models.WarrantyForm.objects.all()
    amount = home_utils.calculate_total_amount_of_this_year_forms(user_all_forms)
    calculate_monthly_amount_for_chart = home_utils.calculate_monthly_amount_of_this_year_forms(user_all_forms)
    calculate_monthly_quantity_for_chart = home_utils.calculate_monthly_quantity_of_this_year_forms(user_all_forms)

    context = {
        'segment': 'index',
        'paid_amount': amount.get("paid_amount"),
        'total_forms': amount.get("total_forms"),
        'chart_data_amount_wise': calculate_monthly_amount_for_chart,
        'chart_data_quantity_wise': calculate_monthly_quantity_for_chart,
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def my_forms(request):
    user_all_forms = home_models.WarrantyForm.objects.all()
    table = home_tables.WarrantyFormTable(user_all_forms)
    amount = home_utils.calculate_total_amount_of_this_year_forms(user_all_forms)
    context = {
        'segment': 'index',
        'table': table,
        'paid_amount': amount.get("paid_amount"),
    }
    return render(request, 'home/table_view.html', context)


@login_required(login_url="/login/")
def add_new_warranty_forms(request):
    form = home_forms.WarrantyForm()
    if request.method == 'POST':
        form = home_forms.WarrantyForm(request.POST)
        obj = None
        if form.is_valid():
            obj = form.save()
            if request.FILES:
                obj.invoice_file = request.FILES.get('invoice_file')
            obj.user = request.user
            obj.save()
            home_utils.send_email_to_user(request.user, obj)
            messages.success(request, f'Form Submitted & Email sent to {obj.customer_name or obj.Last_Name}')
            return redirect('my-forms')
    context = {'segment': 'index', 'form': form}
    return render(request, 'home/add_or_edit.html', context)


@login_required(login_url="/login/")
def export_all_forms(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    response = home_utils.export_all_forms(start_date, end_date)
    return response


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except Exception:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
