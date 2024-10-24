from django.urls import path # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from .views import RegistrationView, UsernameValidationView, VerificationView, EmailValidationView, LoginView, LogoutView, ResetPassword, CompletePasswordReset

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("validate-username", csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path("validate-email", csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path("activate/<uidb64>/<token>", VerificationView.as_view(), name="activate"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("reset-password", csrf_exempt(ResetPassword.as_view()), name="reset-password"),
    path("set-new-password/<uidb64>/<token>", csrf_exempt(CompletePasswordReset.as_view()), name="set-new-password")
]