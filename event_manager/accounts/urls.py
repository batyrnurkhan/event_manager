from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.views import LogoutView
from .views import ClientListView, UserListView, ClientCreateView, ClientDetailView, UserDetailView, ClientUpdateView, \
    ClientDeleteView, ChatListView, ChatDetailView, ensure_chat_rooms
from .views import SuperuserListView, SuperuserDetailView, AddAdminView, EditAdminView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from django.urls import path

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

    path('chats/', ChatListView.as_view(), name='chat_list'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('ensure-chat-rooms/', ensure_chat_rooms, name='ensure_chat_rooms'),
    path('chats/<int:pk>/send/', views.send_message, name='send_message'),  # Add this line

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]

