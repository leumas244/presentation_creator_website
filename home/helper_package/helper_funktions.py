import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
import datetime
import pytz

from home.models import Sended_Email, AdminSetting
from django.urls import reverse


def send_mail(receiver_name, receiver_mail, message, subject):
    admin_settings = AdminSetting.objects.get(id=1)
    try:
        msg = EmailMessage() 
        msg["Subject"] = subject
        msg["From"] = Address(admin_settings.email_user_name , addr_spec=admin_settings.email_user) 
        msg["To"] =  Address(receiver_name , addr_spec=receiver_mail)

        msg.set_content(message)
    
        server = smtplib.SMTP('smtp.strato.de', 587)
        server.starttls()
        server.login(admin_settings.email_user, admin_settings.email_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()

        # create a database entry
        mail_entry = Sended_Email(receiver_mail=msg["To"], sender_mail=msg["From"], subject=msg["Subject"], content=msg.as_string(), send_status=True)
        mail_entry.save()

    except Exception as e:
        error = str(e)
        mail_entry = Sended_Email(receiver_mail=msg["To"], sender_mail=msg["From"], subject=msg["Subject"], content=msg.as_string(), send_status=False, error_massage=error)
        mail_entry.save()


def send_exeption_mail(traceback_details, username):
    admin_settings = AdminSetting.objects.get(id=1)
    now = datetime.datetime.now()
    timezone = pytz.timezone("Europe/Berlin")
    right_time = pytz.utc.localize(now, is_dst=None).astimezone(timezone)
    mail_massage = "Hallo Samuel,\n\nEs gibt ein Problem bei der Präsentation-Webseite von der Stadtmission Grünstadt.\n\n" + "filename:  " + traceback_details['filename'] + "\nlinenumber:  " + traceback_details['lineno'] + "\nname:  " + traceback_details['name'] + "\ntype:  " + traceback_details['type'] + "\nmessage:  " + traceback_details['message'] + "\n\nAusgelöst von: " + str(username) + "\n\nProblem aufgetreten am: " + right_time.strftime("%d.%m.%Y, %H:%M:%S Uhr") + "\n\nViele Grüße\nAdmin"
    subject = "Problem bei der Präsentation-Webseite"
    send_mail(admin_settings.name_error_reciever, admin_settings.email_error_receiver, mail_massage, subject)


def send_exeption_mail_by_automatic_script(traceback_details):
    admin_settings = AdminSetting.objects.get(id=1)
    now = datetime.datetime.now()
    timezone = pytz.timezone("Europe/Berlin")
    right_time = pytz.utc.localize(now, is_dst=None).astimezone(timezone)
    mail_massage = "Hallo Samuel,\n\nEs gibt ein Problem beim Ausführen eines automatischen Skriptes bei der Präsentation-Webseite von der Stadtmission Grünstadt.\n\n" + "filename:  " + traceback_details['filename'] + "\nlinenumber:  " + traceback_details['lineno'] + "\nname:  " + traceback_details['name'] + "\ntype:  " + traceback_details['type'] + "\nmessage:  " + traceback_details['message'] + "\n\nProblem aufgetreten am: " + right_time.strftime("%d.%m.%Y, %H:%M:%S Uhr") + "\n\nViele Grüße\nAdmin"
    subject = "Problem beim Ausführen eines automatischen Skriptes"
    send_mail(admin_settings.name_error_reciever, admin_settings.email_error_receiver, mail_massage, subject)


def send_invation_mail(username, first_name, last_name, email, token):
    login_link = 'http://127.0.0.1:8000' + reverse('login_with_token', args=[token])
    full_name = f'{first_name} {last_name}'
    subject = f'Einladung zur Stadtmission Grünstadt Präsentations-Webseite'
    mail_massage = f'Hallo {first_name},\n\ndu wurdest für die Präsentations-Webseite der Stadtmission Grünstadt registriert. In dieser Mail erhälst du ein Einladungslink zum erstellen deines Passwortes.\nDein Username ist: "{username}"\nEinladungslink: {login_link}\nDieser Link ist eine Woche gültig!\n\nViele Grüße\ndein Admin'
    send_mail(full_name, email, mail_massage, subject)


def send_reset_mail(first_name, last_name, email, token):
    login_link = 'http://127.0.0.1:8000' + reverse('login_with_token', args=[token])
    full_name = f'{first_name} {last_name}'
    subject = f'Passwort zurücksetzen bei der Stadtmission Grünstadt Präsentations-Webseite'
    mail_massage = f'Hallo {first_name},\n\ndu hast dein Passwort zurückgesetzt. Unter dem folgendem Link kannst du dein Passwort zurücksetzen\n {login_link}\nDieser Link ist eine Woche gültig!\n\nViele Grüße\ndein Admin'
    send_mail(full_name, email, mail_massage, subject)
