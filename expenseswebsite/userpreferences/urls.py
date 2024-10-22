from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name="preferences"),
    path('account', views.account_settings, name="account")
]