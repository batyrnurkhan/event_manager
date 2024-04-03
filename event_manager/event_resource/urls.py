from django.urls import path
from .views import *

app_name = 'event_resource'

urlpatterns = [
    path('add_resource/', add_resource, name='add_resource'),
    path('resource_list/', resource_list, name='resource_list'),
    path('edit_resource/<int:id>/', edit_resource, name='edit_resource'),

]
