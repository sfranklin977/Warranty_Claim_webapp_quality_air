from django.urls import path
from apps.rma import views

urlpatterns = [
    path('parts-returns/', views.parts_return_list, name='parts-return-list'),
    path('parts-returns/add/', views.parts_return_add, name='parts-return-add'),
    path('parts-returns/<int:pk>/edit/', views.parts_return_edit, name='parts-return-edit'),
    path('parts-returns/export/', views.parts_return_export, name='parts-return-export'),
]
