import django_tables2 as tables
from . import models as rma_models


class PartsReturnTable(tables.Table):
    class Meta:
        attrs = {
            "class": 'table table-sm table-stripped data-table',
        }
        model = rma_models.PartsReturn
        fields = [
            'client_name',
            'order_number',
            'rma_number',
            'date_rma_requested',
            'date_rma_credit_received',
            'rma_credit_received',
            'model_number',
            'serial_number',
            'invoice_amount',
            'replacement_order_number',
        ]
