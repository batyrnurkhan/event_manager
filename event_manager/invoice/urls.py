from django.urls import path
from .views import *

app_name = 'invoice'

urlpatterns = [
    path('add_invoice/', add_invoice, name='add_invoice'),
    path('list_invoices/', list_invoices, name='list_invoices'),
]
