from django.db import models


class Service(models.Model):
    service_name = models.CharField(max_length=30)
    service_description = models.TextField()
    min_price = models.FloatField()
    number_of_people = models.CharField(max_length=20)
    big_photo = models.ImageField(upload_to='services')
    little_photo = models.ImageField(upload_to='services')
