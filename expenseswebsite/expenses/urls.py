from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('expense-add', views.add_expense, name="add-expense"),
    path('expense-edit/<int:id>', views.edit_expense, name="edit-expense"),
    path('expense-delete/<int:id>', views.delete_expense, name="delete-expense"),
    path('expense-search', csrf_exempt(views.search_expense), name="expense-search")
]