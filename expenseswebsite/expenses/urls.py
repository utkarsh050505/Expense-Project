from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('expense-add', views.add_expense, name="add-expense"),
    path('expense-edit/<int:id>', views.edit_expense, name="edit-expense"),
    path('expense-delete/<int:id>', views.delete_expense, name="delete-expense")
]