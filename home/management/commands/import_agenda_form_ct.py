
from django.core.management.base import BaseCommand
from home.models import WeekMotto


class Command(BaseCommand):
    help = 'Import automatically agendas from CT to database'

    def handle(self, *args, **options):

        pass
