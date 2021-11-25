from datetime import datetime
import jicson
from django.core.management.base import BaseCommand
from home.models import *


class Command(BaseCommand):
    help = 'Create automaticly calender entries with bible passages'

    def handle(self, *args, **options):
        result = jicson.fromFile('home/churchtools_connection_package/data/daskirchenjahr_2019-2020.ics')

        godilist = []

        for item in result['VCALENDAR'][0]['VEVENT']:
            start_date = datetime.strptime(item['DTSTART;VALUE=DATE'], '%Y%m%d')
            end_date = datetime.strptime(item['DTEND;VALUE=DATE'], '%Y%m%d')
            desc = item['DESCRIPTION']
            desc_split = desc.split('\\n')
            spruch = 'no spruch found'
            for piece in desc_split:
                if 'Spruch:' in piece:
                    spruch = piece.replace('Spruch: ', '')

            godi = [item['SUMMARY'], start_date, end_date, spruch]
            godilist.append(godi)

        for god in godilist:
            print(god)
