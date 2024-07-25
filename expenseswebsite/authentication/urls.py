from django.urls import path # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from .views import RegistrationView, UsernameValidationView

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("validate-username", csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
]