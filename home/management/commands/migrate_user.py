from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Migrate Users from other Databases'

    def handle(self, *args, **options):
        user_data = User.objects.get(username='samuel')
        user_data.password = ''
        user_data.save()
