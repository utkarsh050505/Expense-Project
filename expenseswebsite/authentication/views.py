from django.shortcuts import render # type: ignore
from django.views import View # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth.models import User # type: ignore
from validate_email import validate_email # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from django.shortcuts import redirect # type: ignore
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError # type: ignore
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode # type: ignore
from django.contrib.sites.shortcuts import get_current_site # type: ignore
from django.urls import reverse # type: ignore
from django.contrib import auth # type: ignore
from .utils import token_generator
import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Please enter valid Email.'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already in use.'}, status=409)

        return JsonResponse({"email_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters!'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already exists.'}, status=409)

        return JsonResponse({"username_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(username) == 0 or len(email) == 0:
                    return render(request, 'authentication/register.html')
                
                if len(password) < 6:
                    messages.error(request, 'Password should be greater than 6 characters')
                    return render(request, 'authentication/register.html', {
                        'username': username,
                        'email': email
                    })
                

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path-to-view
                    # - getting domain we are on
                    # - relative url to verification
                    # - encode uid
                    # - token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse(
                    'activate',
                    kwargs={
                        'uidb64': uidb64,
                        'token': token_generator.make_token(user)
                    }
                )

                activate_url = 'http://' + domain + link

                email_subject = 'Activate your account'
                email_body = 'Hi ' + user.username + '\n' + 'Please use this link to verify your email - ' + activate_url

                send_mail(
                    email_subject,
                    email_body,
                    "noreply@semicolon.com",
                    [email],
                    fail_silently=False
                )

                messages.success(request, "Account created successfully, Please verify your email")

        return render(request, 'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully!")
            return redirect('login')

        except Exception as e:
            ...

        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('expenses')
            
                messages.error(request, "You need to activate your account, check your Email")
                return render(request, 'authentication/login.html')

            messages.error(request, "Invalid Credentials, Try again")
            return render(request, 'authentication/login.html')
        
        messages.error(request, "Please fill all fields.")
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):

        auth.logout(request)
        return redirect('login')
    
class ResetPassword(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, "Please enter a valid email.")
            return render(request, "authentication/reset-password.html")
        
        user = User.objects.filter(email=email)

        if user.exists():

            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            link = reverse(
                    'set-new-password',
                    kwargs={
                        'uidb64': uidb64,
                        'token': PasswordResetTokenGenerator().make_token(user[0])
                        }
                    )

            reset_url = 'http://' + domain + link

            email_subject = 'Reset your account password'
            email_body = 'Hi there,' + '\n' + 'Please use this link to reset your account password - ' + reset_url

            send_mail(
                email_subject,
                email_body,
                "noreply@semicolon.com",
                [email],
                fail_silently=False
                    )

            messages.success(request, "Please check your email to reset your password")
            return render(request, "authentication/reset-password.html")

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Password link invalid, please try again.")
                return render(request, 'authentication/reset-password.html')
        except Exception as e:
            pass

        return render(request, 'authentication/set-new-password.html', {
            'uidb64': uidb64,
            'token': token
        })
    
    def post(self, request, uidb64, token):

        password = request.POST["password"]
        confirmPassword = request.POST["confirm-password"]

        if password != confirmPassword:
            messages.error(request, "Password does not match.")
            return render(request, 'authentication/set-new-password.html', {
                'uidb64': uidb64,
                'token': token
            })
        
        if len(password) < 6:
            messages.error(request, 'Password should be greater than 6 characters')
            return render(request, 'authentication/set-new-password.html', {
                'uidb64': uidb64,
                'token': token
            })

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successfully")
            return redirect('login')
        except Exception as e:
            messages.error(request, "An unexpected error occurred, Please try again.")
            return render(request, "authentication/set-new-password.html", {
                'uidb64': uidb64,
                'token': token
            })