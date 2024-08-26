from django.shortcuts import render # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .models import Category, Expense
from django.contrib.auth.models import User # type: ignore
from userpreferences.models import UserPreference
from django.shortcuts import redirect # type: ignore
from django.contrib import messages # type: ignore

@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    user_preference = None
    if UserPreference.objects.filter(user=request.user).exists():
        user_preference = UserPreference.objects.get(user=request.user)

    return render(request, 'expenses/index.html', {
        'categories': categories,
        'user_preference': user_preference,
        'expenses': expenses
    })

def add_expense(request):
    categories = Category.objects.all()
    values = request.POST
    user_preference = None
    if UserPreference.objects.filter(user=request.user).exists():
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', {
            'categories': categories,
            'user_preference': user_preference
        })
    
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense_date')

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })
        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })
        if not category:
            messages.error(request, 'Please select a category.')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })
        
        if date:
            Expense.objects.create(amount=amount, date=date, description=description, owner=request.user, category=category)
            messages.success(request, 'Expense saved successfully.')
            return redirect('expenses')
        elif not date:
            Expense.objects.create(amount=amount, description=description, owner=request.user, category=category)
            messages.success(request, 'Expense saved successfully.')
            return redirect('expenses')
    
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', {
            'categories': categories,
            'values': expense
        })
    
    else:
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense_date')

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, 'expenses/edit-expense.html', {
                'categories': categories,
                'values': expense
            })
        if not description:
            messages.error(request, 'Description is required!')
            return render(request, 'expenses/edit-expense.html', {
                'categories': categories,
                'values': expense
            })
        if not category:
            messages.error(request, 'Please select a category.')
            return render(request, 'expenses/edit-expense.html', {
                'categories': categories,
                'values': expense
            })
        
        if date:

            expense.amount = amount
            expense.description = description
            expense.date = date
            expense.category = category
            expense.save()

            messages.success(request, 'Expense edited successfully.')
            return redirect('expenses')
        
        elif not date:

            expense.amount=amount
            expense.description=description
            expense.category=category
            expense.save()

            messages.success(request, 'Expense edited successfully.')
            return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.warning(request, 'Expense removed successfully')
    return redirect('expenses')