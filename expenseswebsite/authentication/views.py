from django.shortcuts import render # type: ignore
from django.views import View # type: ignore

# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')