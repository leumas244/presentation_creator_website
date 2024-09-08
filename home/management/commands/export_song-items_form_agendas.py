import json
import datetime
import progressbar

from django.core.management.base import BaseCommand
from home.models import Agenda


class Command(BaseCommand):
    help = 'Export Users for other databases'

    def handle(self, *args, **options):
        print('######## START EXPORT_SONG-ITEMS_FROM_AGENDAS ########')
        now = datetime.datetime.now()
        time_for_output_file = now.strftime('%d.%m.%Y_%H-%M-%S')
        output_file = f'C:/Users/Samuel/Desktop/song-items_export_from_{time_for_output_file}.json'
        output_dictionary = {}
        list_of_song_items = []
        agendas = Agenda.objects.all()
        counter = 0

        bar = progressbar.ProgressBar(maxval=len(agendas), widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for agenda in agendas:
            content = json.loads(agenda.content)
            if content['data']:
                for item in content['data']['items']:
                    if item['type'] == 'normal':
                        if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
                            if not 'Predigt:' in item['title']:
                                if not ('Predigt' in item['title'] and 'Gebet' in item['title']):
                                    if not ('Ankündigung' in item['title'] or 'Mitglied' in item['title']):
                                        list_of_song_items.append(item['title'])
                        elif 'musikteam' in item["responsible"]["text"].lower():
                            if not item['title'] == 'Gebet':
                                if not ('Gebet' in item['title'] and ':' in item['title']):
                                    list_of_song_items.append(item['title'])

            counter += 1
            bar.update(counter)
        bar.finish()
        
        output_dictionary['song_items'] = list_of_song_items
        try:
            with open(output_file, 'w', encoding='ISO-8859-1') as file:
                json.dump(output_dictionary, file)
        except Exception as e:
            print(f'    Error by write dic in file ({output_file}) with error: "{str(e)}"')

        print('######## END EXPORT_SONG-ITEMS_FROM_AGENDAS ########')

