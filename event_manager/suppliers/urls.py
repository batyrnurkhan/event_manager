from django.urls import path
from .views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView

app_name = 'suppliers'

urlpatterns = [
    path('', SupplierListView.as_view(), name='suppliers_list'),
    path('add/', SupplierCreateView.as_view(), name='suppliers_add'),
    path('<int:pk>/edit/', SupplierUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='delete'),
]
