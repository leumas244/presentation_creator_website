import json
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import AdditionalUserInfo


class Command(BaseCommand):
    help = 'Export Users for other databases'

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        time_for_output_file = now.strftime('%d.%m.%Y_%H-%M-%S')
        output_file = f'C:/Users/Samuel/Desktop/users_export_from_{time_for_output_file}.json'
        output_dictionary = {}
        list_of_users = []
        users = User.objects.all()

        for user in users:
            user_dic = {}
            add_user_info = AdditionalUserInfo.objects.get(user=user)

            user_dic["username"] = user.username
            user_dic["first_name"] = user.first_name
            user_dic["last_name"] = user.last_name
            user_dic["email"] = user.email
            user_dic["password"] = user.password
            user_dic["is_staff"] = user.is_staff
            user_dic["is_superuser"] = user.is_superuser
            user_dic["is_active"] = user.is_active
            user_dic["countdown_file_path"] = add_user_info.countdown_file_path
            user_dic["gender"] = add_user_info.gender

            list_of_users.append(user_dic)
        
        output_dictionary['users'] = list_of_users

        with open(output_file, 'w') as file:
            json.dump(output_dictionary, file)

