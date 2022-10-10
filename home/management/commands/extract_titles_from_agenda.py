import json
import datetime
from multiprocessing.sharedctypes import Value
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

        now = datetime.datetime.now()
        file_path = 'C:/Users/Samuel/Desktop/'
        file_name = 'title_list-' + now.strftime('%d.%m.%Y_%H.%M.%S') + '.csv'
        self.complete_path = file_path + file_name
        self.fuzzy_border = 90
        self.songbook_border = 25

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        print('[' + str(now) + ']')

        header_line = 'Id; Titel; Titel ohne Header; eigene Funde; fuzzy_pattern; end_result'

        outfile = open(self.complete_path, 'a')
        outfile.write(header_line + '\n')
        outfile.close()

        tracked_events = Agenda.objects.all()
        started = False
        while not started:
            event = random.choice(tracked_events)
            church_tools_id = event.church_tools_id
            if event.agenda_state:
                started = True
                print('ID: ' + str(church_tools_id))
                agenda = event.content
                agenda_dictionary = json.loads(agenda)

                for item in agenda_dictionary['data']['items']:
                    if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
                        if ":" in item['title']:
                            self.song_converter(item, church_tools_id)
                        else:
                            with open(self.complete_path, 'a') as outfile:
                                line = str(church_tools_id) + '; ' + item['title'] + '; konnte nicht geparst werden.'
                                outfile.write(line + '\n')

        now = datetime.datetime.now()
        print('[' + str(now) + ']')
        return

    def song_converter(self, item, church_tools_id):
        title = item['title']
        title_split = title.split(':')
        if 'Lied' in title_split[0] or 'lied' in title_split[0]:
            line = str(church_tools_id) + "; "
            title = item['title']
            line = line + title.replace(';', ',-') + "; "
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
                        song_strings.append("{}. {}. {}".format(str(song.id), song.title, str(song.churchSongID)))

                    line = line + str(song_strings) + "; "
                    song_strings = []

                    fuzzy_matches_list = self.fuzzy_pattern(title_without_header)
                    for found in fuzzy_matches_list:
                        fuzzy_value = found[0]
                        song = found[1]
                        song_strings.append("{}. {}. {}. {}".format(fuzzy_value, str(song.id), song.title, str(song.churchSongID)))

                    line = line + str(song_strings) + "; "
                    song_strings = []

                    end_result = self.result_decider(fuzzy_matches_list, songs_founded)
                    for found in end_result:
                        fuzzy_value = found[0]
                        song = found[1]
                        song_strings.append("{}. {}. {}. {}".format(fuzzy_value, str(song.id), song.title, str(song.churchSongID)))

                    line = line + str(song_strings) + "; "

            with open(self.complete_path, 'a') as outfile:
                outfile.write(line + '\n')
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
        if title == '' or title == ' ':
            return []
        hunderter_founds = []
        border_founds = []
        selection_founds = []

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
                hunderter_founds.append([fuzzy_value_lang_1, song])
            elif fuzzy_value_lang_2 == 100:
                hunderter_founds.append([fuzzy_value_lang_2, song])
            elif fuzzy_value_lang_3 == 100:
                hunderter_founds.append([fuzzy_value_lang_3, song])
            elif fuzzy_value_lang_4 == 100:
                hunderter_founds.append([fuzzy_value_lang_4, song])

            elif fuzzy_value_lang_1 > self.fuzzy_border:
                border_founds.append([fuzzy_value_lang_1, song])
            elif fuzzy_value_lang_2 > self.fuzzy_border:
                border_founds.append([fuzzy_value_lang_2, song])
            elif fuzzy_value_lang_3 > self.fuzzy_border:
                border_founds.append([fuzzy_value_lang_3, song])
            elif fuzzy_value_lang_4 > self.fuzzy_border:
                border_founds.append([fuzzy_value_lang_4, song])

            else:
                fuzzy_value_list = [fuzzy_value_lang_1, fuzzy_value_lang_2, fuzzy_value_lang_3, fuzzy_value_lang_4]
                fuzzy_value = max(fuzzy_value_list)
                if len(selection_founds) < 5:
                    selection_founds.append([fuzzy_value, song])
                else: 
                    minmum_value = min(selection_founds, key=lambda item: item[0])
                    if fuzzy_value > minmum_value[0]:
                        selection_founds.remove(minmum_value)
                        selection_founds.append([fuzzy_value, song])

        if hunderter_founds != []:
            return hunderter_founds
        elif border_founds != []:
            return border_founds
        else:
            return selection_founds

        
    def result_decider(self, fuzzy_matches, own_matches):
        if len(own_matches) == 0:
            return fuzzy_matches

        accordance_songs = []
        for own_song in own_matches:
            for fuzzy_song in fuzzy_matches:
                song = fuzzy_song[1]
                if own_song.id == song.id:
                    accordance_songs.append([100, song])
        
        if len(accordance_songs) != 0:
            return accordance_songs
        else:
            return fuzzy_matches
