import re
import os
import sys, traceback
import random
import string
import datetime
import hashlib

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.conf import settings
from django.http import HttpResponse
from .models import AdditionalUserInfo, AdminSetting

from .churchtools_connection_package.churchtoos_api_conection import get_list_of_events, get_agenda_by_event_id
from .churchtools_connection_package.agenda_songbeamer_converter import get_all_necessary_agenda_information, create_songbeamer_file, create_presentation_file
from .helper_package.helper_funktions import send_exeption_mail, send_invation_mail


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
        if add_user_info.has_loged_in:
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
            return redirect('first_login')

    else:
        return redirect('login')


def password_change(request):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        if add_user_info.has_loged_in:
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
            return redirect('first_login')
    else:
        return redirect('login')


def profile_settings(request):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        if add_user_info.has_loged_in:
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
            return redirect('first_login')

    else:
        return redirect('login')


def agenda_by_identifier(request, identifier):
    if request.user.is_authenticated:
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        if add_user_info.has_loged_in:
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
            return redirect('first_login')

    else:
        return redirect('login')

    
def add_user(request):
    if request.user.username == 'samuel' or request.user.username == 'admin':
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        dates = {'add_user_info': add_user_info,}
        if request.method == 'POST':
            try:
                token = token_generator(size=get_random_size())
                first_name = request.POST.get('firstname')
                last_name = request.POST.get('lastname')
                password = hashlib.sha256(token.encode()).hexdigest()
                username = request.POST.get('username')
                email = request.POST.get('email')
                new_user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                new_user.save()

                countdown_file_path = request.POST.get('countdown_file_path')
                gender = request.POST.get('gender')
                token = token_generator(size=get_random_size())
                expiry_date = get_expire_date()
                new_additional_user_info = AdditionalUserInfo(user=new_user, countdown_file_path=countdown_file_path, gender=gender, one_time_token=token, token_expiry_date=expiry_date)
                new_additional_user_info.save()

                send_invation_mail(username, first_name, last_name, email, token)

                messages.success(request, f'Du hast erfolgreich den user "{username}" hinzugefuegt!')
            except:
                messages.error(request, 'Deine Einstellungen konnten nicht geaendert werden!')

            # Seite neuladen
            return redirect('home')
        else:
            return render(request, 'sites/add_user.html', dates)

    else:
        return redirect('login')


def admin_settings(request):
    if request.user.username == 'samuel' or request.user.username == 'admin':
        user = request.user
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        admin_setting = AdminSetting.objects.get(id=1)
        dates = {'add_user_info': add_user_info,
                 'admin_setting': admin_setting,
                 }
        if request.method == 'POST':
            try:
                if request.POST.get('song_folder') != '':
                    admin_setting.song_folder = request.POST.get('song_folder')
                    admin_setting.save()
                if request.POST.get('powerpoin_vorlage') != '':
                    admin_setting.powerpoin_vorlage = request.POST.get('powerpoin_vorlage')
                    admin_setting.save()
                if request.POST.get('base_url') != '':
                    admin_setting.base_url = request.POST.get('base_url')
                    admin_setting.save()
                if request.POST.get('login_token') != '':
                    admin_setting.login_token = request.POST.get('login_token')
                    admin_setting.save()
                if request.POST.get('email_user_name') != '':
                    admin_setting.email_user_name = request.POST.get('email_user_name')
                    admin_setting.save()
                if request.POST.get('email_user') != '':
                    admin_setting.email_user = request.POST.get('email_user')
                    admin_setting.save()
                if request.POST.get('name_error_reciever') != '':
                    admin_setting.name_error_reciever = request.POST.get('name_error_reciever')
                    admin_setting.save()
                if request.POST.get('email_error_receiver') != '':
                    admin_setting.email_error_receiver = request.POST.get('email_error_receiver')
                    admin_setting.save()

                messages.success(request, 'Du hast erfolgreich die Admin-Einstellungen bearbeitet!')
            except:
                messages.error(request, 'Deine Admin-Einstellungen konnten nicht geaendert werden!')

            # Seite neuladen
            return redirect('home')
        else:
            return render(request, 'sites/admin_settings.html', dates)

    else:
        return redirect('login')


def login_with_token(request, token):
    now = datetime.datetime.now()
    try:
        add_user_infos = AdditionalUserInfo.objects.all().exclude(one_time_token=None)
        for add_user_info in add_user_infos:
            if add_user_info.one_time_token == token:
                if now.timestamp() < add_user_info.token_expiry_date.timestamp():
                    login(request, add_user_info.user)
                    return redirect('home')
    except:
        redirect('login')
    return redirect('login')


def first_login(request):
    if request.user.is_authenticated:
        user = request.user
        username = user.username
        add_user_info = AdditionalUserInfo.objects.get(user=user)
        dates = {'add_user_info': add_user_info,}
        if request.method == 'POST':

            password_1 = request.POST.get('new_password1')
            password_2 = request.POST.get('new_password2')

            if password_1 == password_2:
                try:
                    add_user_info.one_time_token = None
                    add_user_info.token_expiry_date = None
                    add_user_info.has_loged_in = True
                    add_user_info.save()

                    user.set_password(password_2)
                    user.save()

                    user_log = User.objects.get(username=username)
                    login(request, user_log)
                    
                    messages.success(request, 'Du hast dein Passwort erfolgreich geändert')
                    return redirect('home')
                except:
                    messages.success(request, 'Dein Passwort konnte NICHT geändert werden.')
                    return render(request, 'sites/first_login.html', dates)
        else:
            return render(request, 'sites/first_login.html', dates)
    else:
        return redirect('login')


def get_expire_date():
    now = datetime.datetime.now()
    return now + datetime.timedelta(weeks=1)


def get_random_size():
    return random.randint(35, 40)


def token_generator(size=40, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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

