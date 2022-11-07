import re
import os
import sys, traceback

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.http import HttpResponse
from .models import AdditionalUserInfo

from .churchtools_connection_package.churchtoos_api_conection import get_list_of_events, get_agenda_by_event_id
from .churchtools_connection_package.agenda_songbeamer_converter import get_all_necessary_agenda_information, create_songbeamer_file, create_presentation_file
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
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        try:
            events = get_list_of_events(mode='short')
            dates = {'events': events,
                     'add_user_info': add_user_info,
                     }

            return render(request, 'sites/home.html', dates)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                         'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                         'lineno'  : str(exc_traceback.tb_lineno),
                         'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                         'type'    : str(exc_type.__name__),
                         'message' : str(exc_value),
                        }
            user = request.user.username
            send_exeption_mail(traceback_details, user)
            error_info = "Leider gibt es ein Server Problem.. Versuche es später nochmal. Eine Mail an den Administrator wurde gesendet."
            dates = {'error_info': error_info}
            return render(request, 'sites/server_error.html', dates)

    else:
        return redirect('login')


def password_change(request):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        dates = {'add_user_info': add_user_info,}
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
                return render(request, 'sites/change_password.html', dates)
        else:
            return render(request, 'sites/change_password.html', dates)

    else:
        return redirect('login')


def profile_settings(request):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        dates = {'add_user_info': add_user_info,}
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

                if request.POST.get('countdown_file_path') != '':
                    add_user_info.countdown_file_path = request.POST.get('countdown_file_path')
                    add_user_info.save()

                messages.success(request, 'Du hast erfolgreich deine Einstellungen geaendert!')
            except:
                messages.error(request, 'Deine Einstellungen konnten nicht geaendert werden!')

            # Seite neuladen
            return redirect('home')
        else:
            return render(request, 'sites/profile_settings.html', dates)

    else:
        return redirect('login')


def agenda_by_identifier(request, identifier):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        try:
            agenda_information = get_all_necessary_agenda_information(identifier)
            dates = {'id': identifier,
                    'agenda_information': agenda_information,
                    'song_counter': 1,
                    'internal_song_counter': 1,
                    'add_user_info': add_user_info,
                    }

            if request.method == 'POST' and 'download_songbeamer_file' in request.POST:
                user = request.user
                id_number = request.POST['download_songbeamer_file']
                songs = {}
                for entry in request.POST:
                    if 'song_number' in entry:
                        row_number = int(entry.replace('song_number', ''))
                        songs[row_number] = request.POST[entry]
                songbeamer_file = create_songbeamer_file(id_number, user, songs)
                download_trigger = download(request, songbeamer_file)
                return download_trigger

            if request.method == 'POST' and 'download_presentation_file' in request.POST:
                user = request.user
                id = request.POST['download_presentation_file']
                presentation_file = create_presentation_file(id, user)
                download_trigger = download(request, presentation_file)
                return download_trigger

            return render(request, 'sites/agenda_by_id.html', dates)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                         'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                         'lineno'  : str(exc_traceback.tb_lineno),
                         'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                         'type'    : str(exc_type.__name__),
                         'message' : str(exc_value),
                        }
            user = request.user.username
            send_exeption_mail(traceback_details, user)
            error_info = "Leider gibt es ein Server Problem.. Versuche es später nochmal. Eine Mail an den Administrator wurde gesendet."
            dates = {'error_info': error_info}
            return render(request, 'sites/server_error.html', dates)

    else:
        return redirect('login')


def base(request):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        dates = {'add_user_info': add_user_info,
                 }

        return render(request, 'sites/base.html', dates)

    else:
        return redirect('login')


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="font/otf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                         'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                         'lineno'  : str(exc_traceback.tb_lineno),
                         'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                         'type'    : str(exc_type.__name__),
                         'message' : str(exc_value),
                        }
            user = request.user.username
            send_exeption_mail(traceback_details, user)
            error_info = "Leider gibt es ein Server Problem.. Versuche es später nochmal. Eine Mail an den Administrator wurde gesendet."
            dates = {'error_info': error_info}
            return render(request, 'sites/server_error.html', dates)

