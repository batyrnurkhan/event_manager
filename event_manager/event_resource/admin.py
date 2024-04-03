from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_id', 'name', 'quantity')
    search_fields = ('name',)
