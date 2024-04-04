from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date_time')
    list_filter = ('amount', 'date_time')

admin.site.register(Invoice, InvoiceAdmin)
