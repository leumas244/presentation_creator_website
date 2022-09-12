import smtplib
import datetime
import pytz

from .settings import email_password, email_user, email_error_receiver
from home.models import Sended_Email


def send_mail(receiver_mail, message, subject):
    mail_text = message

    email_data = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (email_user, receiver_mail, subject, mail_text)

    try:
        server = smtplib.SMTP('smtp.strato.de', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, receiver_mail, email_data)
        server.quit()

        # create a database entry
        mail_entry = Sended_Email(receiver_mail=receiver_mail, sender_mail=email_user, subject=subject, content=mail_text, send_status=True)
        mail_entry.save()

    except Exception as e:
        mail_entry = Sended_Email(receiver_mail=receiver_mail, sender_mail=email_user, subject=subject, content=mail_text, send_status=False, error_message=str(e))
        mail_entry.save()


def send_exeption_mail(error_message):
    now = datetime.datetime.now()
    timezone = pytz.timezone("Europe/Berlin")
    right_time = pytz.utc.localize(now, is_dst=None).astimezone(timezone)
    mail_massage = "Hallo Samuel,\n\nEs gibt ein Problem bei der Präsentation-Webseite von der Stadtmission Grünstadt\n'" + error_message + "'\nProblem aufgetreten am: " + right_time.strftime("%d/%m/%Y, %H:%M:%S") + "\n\nViele Grüße\nAdmin"
    subject = "Problem bei der Präsentation-Webseite"
    send_mail(email_error_receiver, mail_massage, subject)