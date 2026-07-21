import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from . import models as rma_models
from . import tables as rma_tables
from . import forms as rma_forms


@login_required(login_url="/login/")
def parts_return_list(request):
    all_returns = rma_models.PartsReturn.objects.all()
    table = rma_tables.PartsReturnTable(all_returns)
    context = {
        'segment': 'parts-returns',
        'table': table,
    }
    return render(request, 'rma/parts_return_list.html', context)


@login_required(login_url="/login/")
def parts_return_add(request):
    form = rma_forms.PartsReturnForm()
    if request.method == 'POST':
        form = rma_forms.PartsReturnForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.user = request.user
            obj.save()
            messages.success(request, f'Parts Return RMA {obj.rma_number} added successfully.')
            return redirect('parts-return-list')
    context = {'segment': 'parts-returns', 'form': form, 'action': 'Add'}
    return render(request, 'rma/parts_return_form.html', context)


@login_required(login_url="/login/")
def parts_return_edit(request, pk):
    obj = get_object_or_404(rma_models.PartsReturn, pk=pk)
    form = rma_forms.PartsReturnForm(instance=obj)
    if request.method == 'POST':
        form = rma_forms.PartsReturnForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Parts Return RMA {obj.rma_number} updated successfully.')
            return redirect('parts-return-list')
    context = {'segment': 'parts-returns', 'form': form, 'action': 'Edit', 'obj': obj}
    return render(request, 'rma/parts_return_form.html', context)


@login_required(login_url="/login/")
def parts_return_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="parts_returns.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Client Name', 'Order Number', 'Invoice Amount',
        'Model Number', 'Serial Number',
        'RMA Number', 'Date RMA Requested', 'Date RMA Credit Received',
        'RMA Credit Received', 'Replacement Ordered Date', 'Replacement Order Number',
        'Notes', 'Created At',
    ])
    for obj in rma_models.PartsReturn.objects.all():
        writer.writerow([
            obj.client_name, obj.order_number, obj.invoice_amount,
            obj.model_number, obj.serial_number,
            obj.rma_number, obj.date_rma_requested, obj.date_rma_credit_received,
            obj.rma_credit_received, obj.replacement_ordered_date, obj.replacement_order_number,
            obj.notes, obj.created_at,
        ])
    return response
