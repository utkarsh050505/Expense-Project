from django.shortcuts import render, redirect # type: ignore
from django.core.paginator import Paginator # type: ignore
from .models import Source, Income
from userpreferences.models import UserPreference
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from django.http import JsonResponse # type: ignore
from django.db.models import Q # type: ignore
import datetime
import json

# Create your views here.
@login_required(login_url="/authentication/login")
def index(request):
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    user_preference = None
    if UserPreference.objects.filter(user=request.user).exists():
        user_preference = UserPreference.objects.get(user=request.user)

    return render(request, 'income/index.html', {
        'sources': sources,
        'user_preference': user_preference,
        'income': income,
        'page_obj': page_obj
    })

@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    values = request.POST
    user_preference = None
    if UserPreference.objects.filter(user=request.user).exists():
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'income/add_income.html', {
            'sources': sources,
            'user_preference': user_preference
        })
    
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source = request.POST.get('source')
        date = request.POST.get('income_date')

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'income/add_income.html', {
                'categories': sources,
                'values': values
            })
        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'income/add_income.html', {
                'categories': sources,
                'values': values
            })
        if not source:
            messages.error(request, 'Please select a source.')
            return render(request, 'income/add_income.html', {
                'categories': sources,
                'values': values
            })
        
        if date:
            Income.objects.create(amount=amount, date=date, description=description, owner=request.user, source=source)
            messages.success(request, 'Income saved successfully.')
            return redirect('income')
        elif not date:
            Income.objects.create(amount=amount, description=description, owner=request.user, source=source)
            messages.success(request, 'Income saved successfully.')
            return redirect('income')

@login_required(login_url="/authentication/login")
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    user_preference = None
    if UserPreference.objects.filter(user=request.user).exists():
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'income/edit-income.html', {
            'sources': sources,
            'values': income,
            'user_preference': user_preference
        })
    
    else:
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source = request.POST.get('source')
        date = request.POST.get('income_date')

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'income/edit-income.html', {
                'sources': sources,
                'values': income,
                'user_preference': user_preference
            })
        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'income/edit-income.html', {
                'sources': sources,
                'values': income,
                'user_preference': user_preference
            })
        if not source:
            messages.error(request, 'Please select a source.')
            return render(request, 'income/edit-income.html', {
                'sources': sources,
                'values': income,
                'user_preference': user_preference
            })
        
        if date:

            income.amount = amount
            income.description = description
            income.date = date
            income.source = source
            income.save()

            messages.success(request, 'Income edited successfully.')
            return redirect('income')
        
        elif not date:

            income.amount=amount
            income.description=description
            income.source=source
            income.save()

            messages.success(request, 'Income edited successfully.')
            return redirect('income')

@login_required(login_url="/authentication/login")
def delete_income(request, id):
    expense = Income.objects.get(pk=id)
    expense.delete()
    messages.warning(request, 'Income removed successfully')
    return redirect('income')

@login_required(login_url="/authentication/login")
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        income = Income.objects.filter(
        Q(amount__startswith=search_str, owner=request.user) |
        Q(date__startswith=search_str, owner=request.user) |
        Q(description__icontains=search_str, owner=request.user) |
        Q(source__icontains=search_str)
    )

        data = income.values() 
        return JsonResponse(list(data), safe=False)

@login_required(login_url="/authentication/login")
def income_summary(request):
    todayDate = datetime.date.today()
    sixMonthAgo = todayDate - datetime.timedelta(days=180)
    income = Income.objects.filter(date__gte=sixMonthAgo, date__lte=todayDate, owner=request.user)

    representation = {}

    getCategory = lambda income: income.source
    
    def getCategoryAmount(category):
        amount = 0 
        filterCategory = income.filter(source=category) 
        for item in filterCategory: 
            amount += item.amount 
        return amount
    
    category_list = list(set(map(getCategory, income)))

    for i in income:
        for j in category_list:
            representation[j] = getCategoryAmount(j)
    
    return JsonResponse({'income_category_data': representation}, safe=False)

@login_required(login_url="/authentication/login")
def income_stats(request):
    return render(request, "income/income_stats.html")