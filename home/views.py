from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in

def logout(sender, user, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    messages.success(request, 'Du wurdest ausgeloggt.')


def loginsuccessful(sender, user, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    messages.success(request, 'Hallo ' + str(request.user.first_name) + ', du wurdest erfolgreich eingeloggt.')


user_logged_out.connect(logout)
user_logged_in.connect(loginsuccessful)


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        dates = {}
        messages.success(request, 'Erfolgsnachricht')
        messages.info(request, 'Infonachricht')
        messages.warning(request, 'Warningnachricht')
        messages.error(request, 'Errornachricht')
        return render(request, 'sites/home.html', dates)

    else:
        return redirect('login')
