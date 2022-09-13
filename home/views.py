import re

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth import update_session_auth_hash

from .churchtools_connection_package.churchtoos_api_conection import get_list_of_events, get_agenda_by_event_id
from .churchtools_connection_package.agenda_songbeamer_converter import get_all_necessary_agenda_information
from .helper_package.helper_funktions import send_exeption_mail


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
        try:
            events = get_list_of_events(start="2022-09-05", to="2022-10-05")
            dates = {'events': events}

            return render(request, 'sites/home.html', dates)
        except Exception as e:
            user = request.user.username
            error = str(e)
            send_exeption_mail(error, user)
            error_info = "Leider gibt es eine Server Problem.. Versuche es später nochmal. Eine Mail an den Administrator wurde gesendet."
            dates = {'error_info': error_info}
            return render(request, 'sites/server_error.html', dates)

    else:
        return redirect('login')


def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            my_message = re.search('<ul class="errorlist"><li>(.+?)</li>', str(form))
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Du hast dein Passwort erfolgreich geändert')
                return redirect('home')
            else:
                messages.error(request,
                               str(my_message.group().replace('<ul class="errorlist"><li>', '').replace('</li>', '')))
                return render(request, 'sites/change_password.html')
        else:
            return render(request, 'sites/change_password.html')

    else:
        return redirect('login')


def settings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            users = User.objects.get(first_name=request.user.first_name)
            # Nachnamen aendern und Log eintrag dazu erstellen
            try:
                if request.POST.get('firstname') != '':
                    users.first_name = request.POST.get('firstname')
                    users.save()

                if request.POST.get('lastname') != '':
                    users.last_name = request.POST.get('lastname')
                    users.save()

                # Email aendern und Log eintrag dazu erstellen
                if request.POST.get('email') != '':
                    users.email = request.POST.get('email')
                    users.save()

                messages.success(request, 'Du hast erfolgreich deine Einstellungen geaendert!')
            except:
                messages.error(request, 'Deine Einstellungen konnten nicht geaendert werden!')

            # Seite neuladen
            return redirect('home')
        else:
            return render(request, 'sites/settings.html')

    else:
        return redirect('login')


def agenda_by_identifier(request, identifier):
    if request.user.is_authenticated:
        try:
            agenda_information = get_all_necessary_agenda_information(identifier)
            dates = {'id': identifier,
                    'agenda_information': agenda_information,
                    }

            return render(request, 'sites/agenda_by_id.html', dates)
        except Exception as e:
            user = request.user.username
            error = str(e)
            send_exeption_mail(error, user)
            error_info = "Leider gibt es eine Server Problem.. Versuche es später nochmal. Eine Mail an den Administrator wurde gesendet."
            dates = {'error_info': error_info}
            return render(request, 'sites/server_error.html', dates)

    else:
        return redirect('login')


def base(request):
    if request.user.is_authenticated:
        dates = {}

        return render(request, 'sites/base.html', dates)

    else:
        return redirect('login')

