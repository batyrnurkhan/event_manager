from django.shortcuts import render, redirect
from .forms import InvoiceForm
from .models import Invoice

def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice:list_invoices')
    else:
        form = InvoiceForm()
    return render(request, 'invoice/add_invoice.html', {'form': form})

def list_invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice/list_invoices.html', {'invoices': invoices})
