from django.contrib import admin
from .models import CustomUser, ChatRoom
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ChatRoom)

from django.contrib import admin
from .models import Contact, Client

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',  'phone_number', 'message')
    search_fields = ('name', 'email',  'phone_number')

admin.site.register(Contact, ContactAdmin)
admin.site.register(Client)
