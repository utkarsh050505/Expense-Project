from django.urls import path # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('expense-add', views.add_expense, name="add-expense"),
    path('expense-edit/<int:id>', views.edit_expense, name="edit-expense"),
    path('expense-delete/<int:id>', views.delete_expense, name="delete-expense"),
    path('expense-search', csrf_exempt(views.search_expense), name="expense-search"),
    path('expense-summary', views.expense_summary, name="expense-summary"),
    path('stats', views.expense_stats, name="expense-stats")
]