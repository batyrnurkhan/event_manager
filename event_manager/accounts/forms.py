from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = forms.CharField(max_length=20, required=False, help_text='Optional.')

    class Meta:
        model = CustomUser  # Use your CustomUser model
        fields = ('username', 'email', 'phone', 'password1', 'password2',)


class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search for user')


from .models import Client, CustomUser



class ClientForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, required=False)  # Add this line

    class Meta:
        model = Client
        fields = ['user', 'email']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.all()  # Customize if needed
        # If updating, set phone field initial value
        if self.instance.pk:
            self.fields['phone'].initial = self.instance.user.phone

    def save(self, commit=True):
        instance = super(ClientForm, self).save(commit=False)
        user = instance.user
        user.phone = self.cleaned_data['phone']
        user.save()  # Save the user with the new phone number
        if commit:
            instance.save()
            self.save_m2m()  # In case there are many-to-many fields to save
        return instance


from django.contrib.auth.models import Permission

class AdminCreationForm(UserCreationForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_superuser', 'permissions']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Assuming you want admins to also be staff
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
            user.user_permissions.set(self.cleaned_data['permissions'])
        return user

from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']
