from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.views import LogoutView
from .views import ClientListView, UserListView, ClientCreateView, ClientDetailView, UserDetailView, ClientUpdateView, ClientDeleteView
from .views import SuperuserListView, SuperuserDetailView, AddAdminView, EditAdminView

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('superusers/', SuperuserListView.as_view(), name='superuser_list'),
    path('superusers/<int:pk>/', SuperuserDetailView.as_view(), name='superuser_detail'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
    path('edit-admin/<int:pk>/', EditAdminView.as_view(), name='edit_admin'),
]
