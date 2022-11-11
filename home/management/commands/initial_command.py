import progressbar

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import AdditionalUserInfo, AdminSetting


class Command(BaseCommand):
    help = 'Initial Command befor first run'

    def handle(self, *args, **options):
        print('######## START INITIAL_ADMIN_ACOUNT ########')
        user = User.objects.get(username='admin')

        first_name = 'Admin_Vorname'
        last_name = 'Admin_Nachname'
        gender = 'male'
        one_time_token = None
        token_expiry_date = None
        has_loged_in = True

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        add_user_info = AdditionalUserInfo(user=user, gender=gender, one_time_token=one_time_token, 
                                           token_expiry_date=token_expiry_date, has_loged_in=has_loged_in)
        add_user_info.save()

        
        powerpoint_vorlage = 'home/churchtools_connection_package/data/Gottesdienst_Vorlage_2020.pptx'
        base_url = 'https://stamigruenstadt.church.tools/api/'

        email_user_name = 'Präsentations Webseite'
        email_user = 'admin@praesentation.stadtmission-gruenstadt.de'
        email_password = 'test'

        name_error_reciever = 'test'
        email_error_receiver = 'test@de'

        admin_settings = AdminSetting(powerpoin_vorlage=powerpoint_vorlage, base_url=base_url, email_user_name=email_user_name, email_user=email_user,
                                      email_password=email_password, name_error_reciever=name_error_reciever, email_error_receiver=email_error_receiver)
        admin_settings.save()

        print('######## FINISHING INITIAL_ADMIN_ACOUNT ########')
