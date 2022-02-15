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
        self.books = {}
        self.songs = Song.objects.all()

        now = datetime.datetime.now()
        file_path = 'C:/Users/D0290928/Desktop/'
        file_name = 'title_list-' + now.strftime('%d.%m.%Y_%H.%M.%S') + '.csv'
        self.complete_path = file_path + file_name
        self.fuzzy_border = 90

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        print('[' + str(now) + ']')

        header_line = 'Id; Titel; Titel ohne Header; eigene Funde; fuzzy_pattern, save'

        outfile = open(self.complete_path, 'a')
        outfile.write(header_line + '\n')
        outfile.close()

        tracked_events = Agenda.objects.all()
        started = False
        while not started:
            event = random.choice(tracked_events)
            event = tracked_events[3]
            church_tools_id = event.church_tools_id
            line_start = str(church_tools_id) + '; '
            if event.agenda_state:
                started = True
                print('ID: ' + str(church_tools_id))
                agenda = event.content
                agenda_dictionary = json.loads(agenda)

                for item in agenda_dictionary['data']['items']:
                    if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
                        self.song_converter(church_tools_id, item)
            print()

        self.calculate_all_books()
        self.information['books'] = self.books
        print(self.information)
        now = datetime.datetime.now()
        print('[' + str(now) + ']')
        return

    def song_converter(self, event_id, item):
        title = item['title']
        if ':' in title:
            title_split = title.split(':')
            if 'Lied' in title_split[0] or 'lied' in title_split[0]:
                line = str(event_id) + '; '
                title = item['title']
                line = line + title.replace(';', ',-') + "; "
                print('Titel: ' + title)
                if ':' in title:
                    title_split = title.split(':')
                    if len(title_split) > 0:
                        title_without_header = title_split[1]
                        line = line + title_without_header.replace(';', ',-') + "; "
                        title_without_header = ''
                        for split in title_split:
                            if title_split.index(split) != 0:
                                title_without_header = title_without_header + split

                        songs_founded = self.search_song(title_without_header)
                        song_strings = []
                        for song in songs_founded:
                            song_strings.append('ID: ' + str(song.id) + '  ' + song.title)

                        line = line + str(song_strings) + "; "
                        song_strings = []

                        fuzzy_matches, hunderter = self.fuzzy_pattern(title)
                        for song in fuzzy_matches:
                            song_strings.append('ID: ' + str(song.id) + '  ' + song.title)

                        line = line + str(song_strings) + "; "
                        song_strings = []

                        for song in hunderter:
                            song_strings.append('ID: ' + str(song.id) + '  ' + song.title)

                        line = line + str(song_strings) + "; "

                with open(self.complete_path, 'a') as outfile:
                    outfile.write(line + '\n')
                self.get_books(title)

        else:
            print('Cloud not parse')
        return

    def get_books(self, title):
        list_of_books = ['FJ 1', 'FJ1', 'FJ 2', 'FJ2', 'FJ 3', 'FJ3', 'FJ 4', 'FJ4', 'FJ 5', 'FJ5',
                         'CCLI', 'GL', 'JuF', 'GLB']

        for book in list_of_books:
            if book in title:
                if book in self.books:
                    self.books[book] = self.books[book] + 1
                else:
                    self.books[book] = 0

    def calculate_all_books(self):
        counter = 0
        for book in self.books:
            counter = counter + self.books[book]
        self.books['Gesamt'] = counter
        return

    def search_song(self, title_without_header):
        songs_founded = []
        if ';' in title_without_header:
            title_without_header_split = title_without_header.split(';')
            title = title_without_header_split[0]
            if title[0] == ' ':
                title = title[1:len(title)]
            for song in self.songs:
                if song.title == title:
                    songs_founded.append(song)
        return songs_founded

    def fuzzy_pattern(self, title):
        songs_founded = []
        hunderter_founds = []

        highest = 0
        select = ''

        for song in self.songs:
            fuzzy_value_1 = fuzz.partial_ratio(song.title, title)
            fuzzy_value_2 = fuzz.partial_ratio(song.titleLang2, title)
            fuzzy_value_3 = fuzz.partial_ratio(song.titleLang3, title)
            fuzzy_value_4 = fuzz.partial_ratio(song.titleLang4, title)

            if fuzzy_value_1 == 100 or fuzzy_value_2 == 100 or fuzzy_value_3 == 100 or fuzzy_value_4 == 100:
                hunderter_founds.append(song)

            if fuzzy_value_2 > highest:
                highest = fuzzy_value_2
                print('{} "{}" "{}" "{}" "{}"'.format(fuzzy_value_2, song.id, song.title, song.churchSongID, title))

            if fuzzy_value_1 > self.fuzzy_border or fuzzy_value_2 > self.fuzzy_border or \
                    fuzzy_value_3 > self.fuzzy_border or fuzzy_value_4 > self.fuzzy_border:
                songs_founded.append(song)

        if not songs_founded:
            for song in self.songs:
                fuzzy_value = fuzz.ratio(song.churchSongID, title)
                if fuzzy_value > highest:
                    highest = fuzzy_value
                    print('{} "{}" "{}" "{}" "{}"'.format(fuzzy_value, song.id, song.title, song.churchSongID, title))

        return songs_founded, hunderter_founds
