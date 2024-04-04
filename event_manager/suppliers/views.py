from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Supplier

class SupplierListView(ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'suppliers/supplier_list.html'

class SupplierCreateView(CreateView):
    model = Supplier
    fields = ['name', 'contact_info']
    success_url = reverse_lazy('suppliers:suppliers_list')
    template_name = 'suppliers/supplier_form.html'

class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = ['name', 'contact_info']
    success_url = reverse_lazy('suppliers:suppliers_list')
    template_name = 'suppliers/supplier_form.html'

class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers:suppliers_list')
    template_name = 'suppliers/supplier_confirm_delete.html'
