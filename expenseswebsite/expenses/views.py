from django.shortcuts import render # type: ignore

# Create your views here.
def index(request):
    return render(request, 'expenses/index.html')

def add_expense(request):
    return render(request, 'expenses/add_expense.html')