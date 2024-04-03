from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from .forms import SignUpForm, ClientForm, AdminCreationForm
from django import forms
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user instance but don't commit to the database yet
            user = form.save(commit=False)
            # Since `commit=False`, `form.save()` doesn't save m2m data. For User models, usually, it's not needed.
            # If you had many-to-many fields on your user model that were being set by the form, you would need
            # to call form.save_m2m() here.
            user.save()  # Now save the user instance with all fields

            # No need to call `refresh_from_db()` here unless you need to reload the fields for some reason
            # user.refresh_from_db()  # Reload the instance from the database

            # Authenticate the user and log them in
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # Send a welcome email to the user
            send_mail(
                'Welcome to My App',
                'Thank you for registering. EVENT MANAGER 123312312SNDAJKDHKA',
                'your_gmail_address@gmail.com',
                [user.email],
                fail_silently=False
            )

            # Redirect the user to the homepage
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})



from django.views.generic import ListView, CreateView, DetailView
from .models import Client, CustomUser


class ClientListView(ListView):
    model = Client
    template_name = 'admin/client_list.html'
    context_object_name = 'clients'

class UserListView(ListView):
    model = CustomUser
    template_name = 'admin/user_list.html'
    context_object_name = 'users'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'admin/client_form.html'
    success_url = '/accounts/clients/'  # Adjust the URL as needed

class ClientDetailView(DetailView):
    model = Client
    template_name = 'admin/client_detail.html'
    context_object_name = 'client'

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'admin/user_detail.html'
    context_object_name = 'user'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'admin/client_form.html'
    success_url = '/clients/'


from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'admin/client_confirm_delete.html'
    success_url = reverse_lazy('accounts:client_list')

class SuperuserListView(ListView):
    model = CustomUser
    template_name = 'admin/superuser_list.html'
    context_object_name = 'superusers'

    def get_queryset(self):
        return CustomUser.objects.filter(is_superuser=True)


class SuperuserDetailView(DetailView):
    model = CustomUser
    template_name = 'admin/superuser_detail.html'
    context_object_name = 'superuser'
    queryset = CustomUser.objects.filter(is_superuser=True)


class AddAdminView(CreateView):
    form_class = AdminCreationForm
    template_name = 'admin/add_admin.html'
    success_url = reverse_lazy('accounts:superuser_list')



class EditAdminView(UpdateView):
    model = CustomUser
    form_class = AdminCreationForm  # You might need a slightly modified form for editing
    template_name = 'admin/edit_admin.html'
    success_url = reverse_lazy('accounts:superuser_list')