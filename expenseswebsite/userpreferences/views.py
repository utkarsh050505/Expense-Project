from django.shortcuts import render # type: ignore
import os
import json
from django.conf import settings # type: ignore
from .models import UserPreference

# Create your views here.
def index(request):
    user_preferences_exists = False
    user_preferences = None
    
    # Check if UserPreference exists for the user
    if UserPreference.objects.filter(user=request.user).exists():
        user_preferences = UserPreference.objects.get(user=request.user)
        user_preferences_exists = True

    # Load currency data from JSON file
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})

    if request.method == 'GET':
        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'user_preferences': user_preferences
        })
    
    elif request.method == 'POST':
        # Check if 'currency' is in request.POST
        currency = request.POST.get('currency', None)

        if currency:
            if user_preferences_exists:
                user_preferences.currency = currency
                user_preferences.save()
            else:
                UserPreference.objects.create(user=request.user, currency=currency)
            
            # After saving or creating, fetch the updated preferences
            user_preferences = UserPreference.objects.get(user=request.user)

        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'user_preferences': user_preferences
        })