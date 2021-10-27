from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def home(request):
    dates = {}
    messages.success(request, 'Erfolgsnachricht')
    messages.info(request, 'Infonachricht')
    messages.warning(request, 'Warningnachricht')
    messages.error(request, 'Errornachricht')
    return render(request, 'sites/home.html', dates)
