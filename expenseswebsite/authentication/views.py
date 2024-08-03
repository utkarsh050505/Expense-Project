from django.shortcuts import render # type: ignore
from django.views import View # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth.models import User # type: ignore
from validate_email import validate_email # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
import json

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
                    messages.error(request, 'Password should be greater than or equal to 6')
                    return render(request, 'authentication/register.html', {
                        'username': username,
                        'email': email
                    })

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                email_subject = 'Activate your account'
                email_body = 'Test'

                send_mail(
                    email_subject,
                    email_body,
                    "noreply@semicolon.com",
                    [email],
                    fail_silently=False
                )

                user.save()

                messages.success(request, "Account created successfully :)")

        return render(request, 'authentication/register.html')