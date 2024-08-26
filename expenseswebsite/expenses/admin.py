from django.contrib import admin # type: ignore
from .models import Expense, Category
# Register your models here.

admin.site.register(Expense)
admin.site.register(Category)
