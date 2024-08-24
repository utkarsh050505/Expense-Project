from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.
class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user) + 's' + ' preference'