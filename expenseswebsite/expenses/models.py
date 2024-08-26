from django.db import models # type: ignore
from django.utils.timezone import now # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=250)

    def __str__(self):
        return "Expense: " + str(self.amount) + " Category: " + self.category + " on " + str(self.date)

    class Meta:
        ordering: ['-date']

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
