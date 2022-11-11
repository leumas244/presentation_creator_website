import os
import hashlib
import datetime
import progressbar
import sys

from django.core.management.base import BaseCommand
from home.models import Song, AdminSetting
from home.helper_package.helper_funktions import send_exeption_mail_by_automatic_script


class Command(BaseCommand):
    help = 'Save automatically Songs from .sng files out of Dropboxfolder to Database'

    def handle(self, *args, **options):
        self.print_info('STARTING IMPORT_SNG_FILES_TO_DATABASE')
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
            self.print_info('ENDING IMPORT_SNG_FILES_TO_DATABASE WITH AN ERROR: ' + str(e))
            exit()

        self.print_info('ENDING IMPORT_SNG_FILES_TO_DATABASE')
        print()

    
    def print_info(self, info):
        now_funktion = datetime.datetime.now()
        print(f"[{now_funktion.strftime('%Y/%m/%d %H:%M:%S')}] {info}")


    def start_routine(self):
        used_keywords = ['title', 'copyrights', 'addCopyrightInfo', 'author', 'bible', 'CCLI', 'categories',
                         'churchSongID',
                         'comment', 'editor', 'format', 'key', 'keywords', 'lang', 'langCount', 'melody',
                         'natCopyright',
                         'oTitle', 'quickFind', 'rights', 'songbook', 'speed', 'titleFormat', 'titleLang2',
                         'titleLang3',
                         'titleLang4', 'translation', 'verseOrder', 'version']
        tracked_songs = Song.objects.all()
        admin_settings = AdminSetting.objects.get(id=1)
        songs_path_folder = admin_settings.song_folder

        song_files_path_tree = self.get_song_files_path_tree(songs_path_folder)
        
        list_of_all_song_files = self.get_list_of_all_files(song_files_path_tree, songs_path_folder)
        amount_of_all_song_files = len(list_of_all_song_files)

        list_of_tracked_song_paths = self.get_list_of_tracked_song_paths(tracked_songs)

        counter_done = 0
        counter_updated_file = 0
        counter_not_updated_file = 0
        counter_created_song = 0        
        print('Starting checking every song file')
        bar = progressbar.ProgressBar(maxval=amount_of_all_song_files, widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for song_file_path in list_of_all_song_files:
            if song_file_path in list_of_tracked_song_paths:
                list_of_tracked_song_paths.remove(song_file_path)
                current_database_song = Song.objects.get(filePath=song_file_path)
                database_song_hash = current_database_song.file_md5_hash
                song_file_path_hash = self.get_md5_hash(songs_path_folder + '/' + song_file_path)
                if database_song_hash == song_file_path_hash:
                    counter_not_updated_file += 1
                else:
                    id_number = self.update_song(song_file_path, current_database_song, songs_path_folder, used_keywords)
                    if id_number:
                        counter_updated_file += 1
            else:
                id_number = self.track_new_song_file(song_file_path, songs_path_folder, used_keywords)
                if id_number:
                    counter_created_song += 1
            
            bar.update(counter_done)
            counter_done += 1
        bar.finish()
        print('Finishing checking every song file')

        counter_done = 0
        counter_deleted_songs = 0
        print('Starting deleting old song files')
        bar = progressbar.ProgressBar(maxval=len(list_of_tracked_song_paths), widgets=[progressbar.Bar('=', '    [', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for song_file_path in list_of_tracked_song_paths:
            try:
                delete_song = Song.objects.get(filePath=song_file_path)
                id_number = delete_song.id
                delete_song.delete()
                counter_deleted_songs += 1
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback_details = {'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                                    'lineno'  : str(exc_traceback.tb_lineno),
                                    'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                                    'type'    : str(exc_type.__name__),
                                    'message' : str(exc_value),
                                    }
                send_exeption_mail_by_automatic_script(traceback_details)
                print(f'    Could not delete Song (ID:{song_file_path}). Because of: {str(e)}')
            
            counter_done += 1
            bar.update(counter_done)
        bar.finish()
        print('Finishing deleting old song files')

        print('SUMMARY')
        print('{:<20}   {:<13}   {:<13}   {:<13}   {:<13}'.format('All Songs in Dropbox', 'Created Songs', 'Edit Songs', 'No Edit Songs', 'Deleted Songs'))
        print('-'*84)
        print('{:<20}   {:<13}   {:<13}   {:<13}   {:<13}'.format(amount_of_all_song_files, counter_created_song, counter_updated_file, counter_not_updated_file, counter_deleted_songs))





    def get_song_files_path_tree(self, folder):
        paths = {}
        file_counter = 0
        try:
            for (root, dirs, files) in os.walk(folder):
                sng_files = []

                for file in files:
                    if '.sng' == file[-4:]:
                        sng_files.append(file)

                file_counter = file_counter + len(sng_files)

                if '\\' in str(root):
                    my_root = str(root).replace('\\', '/')
                else:
                    my_root = str(root)

                paths[my_root] = sng_files

            paths['meta'] = {'file_counter': file_counter}
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
            self.print_info('ENDING IMPORT_SNG_FILES_TO_DATABASE (By get_song_files_path_tree) WITH AN ERROR: ' + str(e))
            exit()
        return paths


    def get_list_of_all_files(self, paths, folder):
        all_file_paths = []
        try:
            for path in paths:
                if not len(paths[path]) == 0 and path != 'meta':
                    for song_name in paths[path]:
                        all_file_paths.append((path.replace(folder, '') + '/' + song_name)[1:])
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
            self.print_info('ENDING IMPORT_SNG_FILES_TO_DATABASE (By get_list_of_all_files) WITH AN ERROR: ' + str(e))
            exit()
        return all_file_paths


    def get_md5_hash(self, file_path):
        md5_hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buf = file.read()
        md5_hasher.update(buf)
        file_hash = md5_hasher.hexdigest()
        return file_hash


    def get_list_of_tracked_song_paths(self, songs):
        list_of_tracked_song_paths = []
        for song in songs:
            list_of_tracked_song_paths.append(song.filePath)
        return list_of_tracked_song_paths


    def update_song(self, song_file_path, current_database_song, path_folder, used_keywords):
        complete_file_path = path_folder + '/' + song_file_path
        try:
            keywords, content = self.get_dictionary_of_keywords(complete_file_path)
            md5_hash = self.get_md5_hash(complete_file_path)

            for keyword in keywords:
                if keyword in used_keywords:
                    setattr(current_database_song, keyword, keywords[keyword])

            current_database_song.file_md5_hash = md5_hash
            current_database_song.content = content
            current_database_song.save()
            id_number = current_database_song.id

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                                'lineno'  : str(exc_traceback.tb_lineno),
                                'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                                'type'    : str(exc_type.__name__),
                                'message' : str(exc_value),
                                }
            send_exeption_mail_by_automatic_script(traceback_details)
            print(f'    Could not update Song (ID:{current_database_song.id}). Because of: {str(e)}')
            id_number = None

        return id_number


    def track_new_song_file(self, file_path, path_folder, used_keywords):
        complete_file_path = path_folder + '/' + file_path
        try:
            keywords, content = self.get_dictionary_of_keywords(complete_file_path)
            if 'title' in keywords:
                title = keywords['title']
            else:
                title = 'NO TITLE'
            md5_hash = self.get_md5_hash(complete_file_path)

            new_song = Song(title=title, filePath=file_path, content=content, file_md5_hash=md5_hash)

            for keyword in keywords:
                if keyword in used_keywords:
                    setattr(new_song, keyword, keywords[keyword])
            new_song.save()
            id_number = new_song.id

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                                'lineno'  : str(exc_traceback.tb_lineno),
                                'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                                'type'    : str(exc_type.__name__),
                                'message' : str(exc_value),
                                }
            send_exeption_mail_by_automatic_script(traceback_details)
            print(f'    Could not create new Song. Because of: {str(e)}')
            id_number = None

        return id_number


    def get_dictionary_of_keywords(self, file_path):
        dictionary_of_keywords = {}
        file_opener = open(file_path, 'r', encoding='utf-8')
        file_content = file_opener.read()
        keyword_data = file_content.split('---')[0]
        file_opener.close()

        keyword_data = keyword_data.split('\n')
        for line in keyword_data:
            if line != '':
                if '#' == line[0]:
                    line = line.replace('#', '')
                    line_split = line.split('=')
                    keyword = line_split[0]
                    value = line_split[1]
                    if keyword == '(c)':
                        keyword = 'copyrights'
                    elif keyword == 'CCLI':
                        keyword = 'CCLI'
                        try:
                            int(value)
                        except ValueError:
                            continue
                    else:
                        keyword = keyword[0].lower() + keyword[1:]
                    dictionary_of_keywords[keyword] = value

        return dictionary_of_keywords, file_content
