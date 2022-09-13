import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
import datetime
import pytz

from .settings import email_user_name, email_password, email_user, email_error_receiver, name_error_reciever
from home.models import Sended_Email


def send_mail(receiver_name, receiver_mail, message, subject):
    try:
        msg = EmailMessage() 
        msg["Subject"] = subject
        msg["From"] = Address(email_user_name , addr_spec=email_user) 
        msg["To"] =  Address(receiver_name , addr_spec=receiver_mail)

        msg.set_content(message)
    
        server = smtplib.SMTP('smtp.strato.de', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()

        # create a database entry
        mail_entry = Sended_Email(receiver_mail=msg["To"], sender_mail=msg["From"], subject=msg["Subject"], content=msg.as_string(), send_status=True)
        mail_entry.save()

    except Exception as e:
        error = str(e)
        mail_entry = Sended_Email(receiver_mail=msg["To"], sender_mail=msg["From"], subject=msg["Subject"], content=msg.as_string(), send_status=False, error_massage=error)
        mail_entry.save()


def send_exeption_mail(error_message, username):
    now = datetime.datetime.now()
    timezone = pytz.timezone("Europe/Berlin")
    right_time = pytz.utc.localize(now, is_dst=None).astimezone(timezone)
    mail_massage = "Hallo Samuel,\n\nEs gibt ein Problem bei der Präsentation-Webseite von der Stadtmission Grünstadt.\n\n'" + error_message + "'\n\nAusgelöst von: " + str(username) + "\n\nProblem aufgetreten am: " + right_time.strftime("%d.%m.%Y, %H:%M:%S Uhr") + "\n\nViele Grüße\nAdmin"
    subject = "Problem bei der Präsentation-Webseite"
    send_mail(name_error_reciever, email_error_receiver, mail_massage, subject)