from django.urls import path # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='income'),
    path('income-add', views.add_income, name="add-income"),
    path('income-edit/<int:id>', views.edit_income, name="edit-income"),
    path('income-delete/<int:id>', views.delete_income, name="delete-income"),
    path('income-search', csrf_exempt(views.search_income), name="income-search")
]