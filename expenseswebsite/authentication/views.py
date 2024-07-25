from django.shortcuts import render # type: ignore
from django.views import View # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth.models import User # type: ignore
import json

# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters!'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already exists.'}, status=409)

        return JsonResponse({"username_valid": True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')