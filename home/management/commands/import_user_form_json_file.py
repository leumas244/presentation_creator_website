import json
import datetime
import progressbar

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import AdditionalUserInfo


class Command(BaseCommand):
    help = 'Migrate Users from other Databases'

    def handle(self, *args, **options):
        print('######## START IMPORT_USERS_FROM_JSON_FILE ########')
        json_file = f'C:/Users/Samuel/Desktop/users_export_from_11.11.2022_18-30-36.json'

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f'    Error by load dic from file ({json_file}) with error: "{str(e)}"')
            exit()

        users = data['users']
        counter = 0

        bar = progressbar.ProgressBar(maxval=len(users), widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for user in users:
            username = user["username"]
            first_name = user["first_name"]
            last_name = user["last_name"]
            email = user["email"]
            password = user["password"]
            is_staff = user["is_staff"]
            is_superuser = user["is_superuser"]
            is_active = user["is_active"]
            countdown_file_path = user["countdown_file_path"]
            gender = user["gender"]
            one_time_token = user["one_time_token"]
            token_expiry_date = user["token_expiry_date"]
            if token_expiry_date is not None:
                token_expiry_date = datetime.datetime.fromtimestamp(token_expiry_date)
            has_loged_in = user["has_loged_in"]


            tracked_user = User.objects.filter(username=username)
            
            if not tracked_user:
                created_user = User.objects.create_user(username, email, 'Test1234')
                created_user.first_name = first_name
                created_user.last_name = last_name
                created_user.password = password
                created_user.is_active = is_active
                created_user.is_staff = is_staff
                created_user.is_superuser = is_superuser
                created_user.save()

                add_user_info = AdditionalUserInfo(user=created_user, countdown_file_path=countdown_file_path, gender=gender, 
                                                   one_time_token=one_time_token, token_expiry_date=token_expiry_date, has_loged_in=has_loged_in)
                add_user_info.save()
                
                print(f'    Created User: {username} ({created_user.id})')
            counter += 1
            bar.update(counter)
        bar.finish()

        print('######## FINISHING IMPORT_USERS_FROM_JSON_FILE ########')
