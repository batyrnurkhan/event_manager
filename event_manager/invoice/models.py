from django.db import models

class Invoice(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"Invoice {self.id}: Amount - {self.amount}, Date and Time - {self.date_time}"
