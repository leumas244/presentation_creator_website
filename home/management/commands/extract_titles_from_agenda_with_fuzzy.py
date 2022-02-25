import json
import datetime
import random
from fuzzywuzzy import fuzz

from django.core.management.base import BaseCommand
from home.models import Agenda, Song


class Command(BaseCommand):
    help = 'Import automatically agendas from CT to database'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.information = {}
        self.songs = Song.objects.all()
        self.tracked_events = Agenda.objects.all()

        self.fuzzy_border = 80

    def handle(self, *args, **options):
        start_time = datetime.datetime.now()
        print('[' + start_time.strftime('%d.%m.%Y_%H.%M.%S') + ']')

        event = random.choice(self.tracked_events)
        church_tools_id = event.church_tools_id

        if event.agenda_state:
            print('ID: ' + str(church_tools_id))
            agenda = event.content
            agenda_dictionary = json.loads(agenda)

            for item in agenda_dictionary['data']['items']:
                if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
                    print('ITEM: "' + item['title'] + '"')
                    self.song_converter(church_tools_id, item)
                    print()

        end_time = datetime.datetime.now()
        time_delta = end_time - start_time
        print('[' + end_time.strftime('%d.%m.%Y_%H.%M.%S') + '] (' + str(time_delta) + ')')
        return

    def song_converter(self, event_id, item):
        title = item['title']

        if ':' in title:
            title_split = title.split(':')
            if 'Lied' in title_split[0] or 'lied' in title_split[0]:
                title_without_header = ''
                for split in title_split:
                    if title_split.index(split) != 0:
                        title_without_header = title_without_header + split
                hundred, border_songs, selected_song = self.fuzzy_pattern(title_without_header)

                print('AUSGEWÄLT:')
                if hundred:
                    song = hundred[0]
                    print('{}; {}'.format(song.title, song.churchSongID))
                    return song

                elif border_songs:
                    if len(border_songs) == 1:
                        song = list(border_songs)[0]
                        fuzzy_value = border_songs[song]
                        print('{} {}; {}'.format(fuzzy_value, song.title, song.churchSongID))
                        return song
                    else:
                        highest = 0
                        select = None
                        for song in border_songs:
                            if border_songs[song] > highest:
                                highest = border_songs[song]
                                select = song
                        print('{} {}; {}'.format(highest, select.title, select.churchSongID))
                        return select
                else:
                    fuzzy_value = list(selected_song)[0]
                    song = selected_song[fuzzy_value]
                    print('{} {}; {}'.format(fuzzy_value, song.title, song.churchSongID))
                    return song

        else:
            print('Problem! Kein Doppelpunkt gefunden!')
            return

    def fuzzy_pattern(self, title):
        fuzzy_founds = []
        hunderter_founds = []

        hundred = []
        border_dictionary = {}
        selected_dictionary = {}

        highest = 0
        selected_song = ''

        for song in self.songs:
            fuzzy_value_lang_2 = 0
            fuzzy_value_lang_3 = 0
            fuzzy_value_lang_4 = 0

            if song.churchSongID:
                title_lang_1 = song.title + '; ' + song.churchSongID
            else:
                title_lang_1 = song.title
            fuzzy_value_lang_1 = fuzz.token_sort_ratio(title_lang_1.lower(), title.lower())
            if song.titleLang2:
                if song.churchSongID:
                    title_lang_2 = song.titleLang2 + '; ' + song.churchSongID
                else:
                    title_lang_2 = song.titleLang2
                fuzzy_value_lang_2 = fuzz.token_sort_ratio(title_lang_2.lower(), title.lower())
            if song.titleLang3:
                if song.churchSongID:
                    title_lang_3 = song.titleLang3 + '; ' + song.churchSongID
                else:
                    title_lang_3 = song.titleLang3
                fuzzy_value_lang_3 = fuzz.token_sort_ratio(title_lang_3.lower(), title.lower())
            if song.titleLang4:
                if song.churchSongID:
                    title_lang_4 = song.titleLang4 + '; ' + song.churchSongID
                else:
                    title_lang_4 = song.titleLang4
                fuzzy_value_lang_4 = fuzz.token_sort_ratio(title_lang_4.lower(), title.lower())

            if fuzzy_value_lang_1 == 100:
                hunderter_founds.append('{}; {}'.format(song.title, song.churchSongID))
                hundred.append(song)
            elif fuzzy_value_lang_2 == 100:
                hunderter_founds.append('{}; {}'.format(song.titleLang2, song.churchSongID))
                hundred.append(song)
            elif fuzzy_value_lang_3 == 100:
                hunderter_founds.append('{}; {}'.format(song.titleLang3, song.churchSongID))
                hundred.append(song)
            elif fuzzy_value_lang_4 == 100:
                hunderter_founds.append('{}; {}'.format(song.titleLang4, song.churchSongID))
                hundred.append(song)

            elif fuzzy_value_lang_1 > self.fuzzy_border:
                fuzzy_founds.append('{} {}; {}'.format(fuzzy_value_lang_1, song.title, song.churchSongID))
                border_dictionary[song] = fuzzy_value_lang_1
            elif fuzzy_value_lang_2 > self.fuzzy_border:
                fuzzy_founds.append('{} {}; {}'.format(fuzzy_value_lang_2, song.titleLang2, song.churchSongID))
                border_dictionary[song] = fuzzy_value_lang_2
            elif fuzzy_value_lang_3 > self.fuzzy_border:
                fuzzy_founds.append('{} {}; {}'.format(fuzzy_value_lang_3, song.titleLang3, song.churchSongID))
                border_dictionary[song] = fuzzy_value_lang_3
            elif fuzzy_value_lang_4 > self.fuzzy_border:
                fuzzy_founds.append('{} {}; {}'.format(fuzzy_value_lang_4, song.titleLang4, song.churchSongID))
                border_dictionary[song] = fuzzy_value_lang_4

            else:
                fuzzy_value_list = [fuzzy_value_lang_1, fuzzy_value_lang_2, fuzzy_value_lang_3, fuzzy_value_lang_4]
                for fuzzy_value in fuzzy_value_list:
                    if fuzzy_value > highest:
                        highest = fuzzy_value
                        selected_dictionary = {fuzzy_value: song}
                        if highest == fuzzy_value_lang_1:
                            selected_song = '{} {}; {}'.format(fuzzy_value_lang_1, song.title, song.churchSongID)
                        if highest == fuzzy_value_lang_2:
                            selected_song = '{} {}; {}'.format(fuzzy_value_lang_2, song.titleLang2, song.churchSongID)
                        if highest == fuzzy_value_lang_3:
                            selected_song = '{} {}; {}'.format(fuzzy_value_lang_3, song.titleLang3, song.churchSongID)
                        if highest == fuzzy_value_lang_4:
                            selected_song = '{} {}; {}'.format(fuzzy_value_lang_4, song.titleLang4, song.churchSongID)

        # print('Hundertprozentige Funde')
        # print(hunderter_founds)
        # print('Border funde:')
        # print(fuzzy_founds)
        # print('Höchster Wert')
        # print(selected_song)

        return hundred, border_dictionary, selected_dictionary
