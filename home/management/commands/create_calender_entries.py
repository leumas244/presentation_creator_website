from datetime import datetime
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from home.models import WeekMotto


class Command(BaseCommand):
    help = 'Create automaticly calender entries with bible passages'

    def handle(self, *args, **options):
        source_file = open('home/churchtools_connection_package/data/jahr_2021-2022.html')
        soup = BeautifulSoup(source_file, features="html.parser")
        source_file.close()

        rows = soup.findAll('tr')

        for row in rows[1:]:
            fields = row('td')

            title = fields[0].contents[0]
            date = datetime.strptime(fields[1].contents[0][0:10], '%d.%m.%Y')
            gospels = fields[2].contents[0]
            epistle = fields[3].contents[0]
            old_testament = fields[4].contents[0]
            lecture = fields[5].contents[0]
            motto_short = fields[6].contents[0]
            motto_long = ''
            motto_api = ''

            week_motto = WeekMotto(title=title, date=date, gospels=gospels, epistle=epistle,
                                   old_testament=old_testament, lecture=lecture, motto_short=motto_short,
                                   motto_long=motto_long, motto_api=motto_api)
            week_motto.save()
