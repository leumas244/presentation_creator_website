import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import AdditionalUserInfo


class Command(BaseCommand):
    help = 'Migrate Users from other Databases'

    def handle(self, *args, **options):
        json_file = f'C:/Users/Samuel/Desktop/test.json'

        with open(json_file, 'r') as file:
            data = json.load(file)

        users = data['users']

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

                add_user_info = AdditionalUserInfo(user=created_user, countdown_file_path=countdown_file_path, gender=gender)
                add_user_info.save()
                
                print(f'Created User: {username} ({created_user.id})')
