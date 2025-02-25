import json
import requests
import datetime
import sys

from django.core.management.base import BaseCommand
from home.models import Song
from home.churchtools_connection_package.settings import login_token, base_url
from home.helper_package.helper_funktions import send_exeption_mail_by_automatic_script, send_mail_for_missing_song


class Command(BaseCommand):
    help = 'Initial Command befor first run'

    def handle(self, *args, **options):
        self.print_info('######## STARTING Comparing Songs from CT with local DB ########')
        try:
            self.start_routine()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                         'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                         'lineno'  : str(exc_traceback.tb_lineno),
                         'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                         'type'    : str(exc_type.__name__),
                         'message' : str(exc_value),
                        }
            send_exeption_mail_by_automatic_script(traceback_details)
            self.print_info('ENDING IMPORTING_AGENDA_FROM_CHURCHTOOLS WITH AN ERROR: ' + str(e))
            exit()

        self.print_info('######## FINISHING Comparing Songs from CT with local DB ########')

    def start_routine(self):
        churchtools_songs_data = self.get_songs_with_limit(limit=200)
        churchtools_songs = churchtools_songs_data['data']

        tracked_songs = Song.objects.all()

        churchtools_songs_with_no_ccli_match = []
        for churchtools_song in churchtools_songs:
            ccli_match = False
            chruchtools_song_ccli = churchtools_song['ccli']
            for tracked_song in tracked_songs:
                if tracked_song.CCLI == int(chruchtools_song_ccli):
                    ccli_match = True
            if not ccli_match:
                churchtools_songs_with_no_ccli_match.append(churchtools_song)

        self.print_info(info=f'Songs with no macht:')
        for song in churchtools_songs_with_no_ccli_match:
            self.print_info(info=f'- {song['name']}; CCLI: {song['ccli']}; CT-SongId: {song['id']}', tab=8, date=False)

        if churchtools_songs_with_no_ccli_match:
            send_mail_for_missing_song(churchtools_songs_with_no_ccli_match)

    def print_info(self, info, tab = 0, date = True):
        now_variable = datetime.datetime.now()
        if date:
            print(f"[{now_variable.strftime('%Y/%m/%d %H:%M:%S')}] {'   '*tab}{info}")
        else:
            print(f"{'   '*tab}{info}")

    def request_to_church_tools(self, url):
        login_token_url = 'login_token=' + login_token
        response = requests.get(base_url + url + login_token_url)

        data = json.loads(response.text)
        return data

    def get_songs_with_limit(self, limit: int = 100):
        get_songs_url = "songs?page=1&limit=" + str(limit) + "&"

        data = self.request_to_church_tools(get_songs_url)
        return data
