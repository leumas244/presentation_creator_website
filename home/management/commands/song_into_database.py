import os
import hashlib

from django.core.management.base import BaseCommand
from home.models import Song


class Command(BaseCommand):
    help = 'Save automatically Songs from .sng files to Database'

    def handle(self, *args, **options):
        used_keywords = ['title', 'copyrights', 'addCopyrightInfo', 'author', 'bible', 'CCLI', 'categories',
                         'churchSongID',
                         'comment', 'editor', 'format', 'key', 'keywords', 'lang', 'langCount', 'melody',
                         'natCopyright',
                         'oTitle', 'quickFind', 'rights', 'songbook', 'speed', 'titleFormat', 'titleLang2',
                         'titleLang3',
                         'titleLang4', 'translation', 'verseOrder', 'version']
        path_folder = 'D:/Dropbox/Songs'
        tracked_songs = Song.objects.all()
        song_file_path_tree = self.get_all_paths(path_folder)
        if not song_file_path_tree:
            print('FAILURE - Getting all file path')
            return
        list_of_all_song_files = self.get_list_of_all_files(song_file_path_tree, path_folder)
        if not list_of_all_song_files:
            print('FAILURE - Getting list of all files')
            return

        print('        STARTING - Viewing every single song-file')
        list_of_tracked_songs = self.get_list_of_tracked_songs(tracked_songs)
        for song_file_path in list_of_all_song_files:
            print('[' + str((round(
                ((list_of_all_song_files.index(song_file_path) + 1) / len(list_of_all_song_files)) * 100, 1))) + '%]')

            if song_file_path in list_of_tracked_songs:
                list_of_tracked_songs.remove(song_file_path)
                current_database_song = Song.objects.get(filePath=song_file_path)
                database_song_hash = current_database_song.file_md5_hash
                song_file_path_hash = self.get_md5_hash(path_folder + '/' + song_file_path)
                if database_song_hash == song_file_path_hash:
                    print('        Song "' + song_file_path + '" has no update')
                    continue
                else:
                    id_number = self.update_song(song_file_path, current_database_song, path_folder, used_keywords)
                    if not id_number:
                        print('FAILURE - Updating database_file')
                        return
                    print('        Song "' + song_file_path + '" updated with id: ' + str(id_number))
            else:
                id_number = self.track_new_song_file(song_file_path, path_folder, used_keywords)
                if not id_number:
                    print('FAILURE - Creating database_file')
                    return
                print('        Song "' + song_file_path + '" created with id: ' + str(id_number))
        print('        ENDING - Viewing every single song-file')
        print('        STARTING - Deleting old database entries with no file')
        for song_file_path in list_of_tracked_songs:
            print('[' + str((round(
                ((list_of_tracked_songs.index(song_file_path) + 1) / len(list_of_tracked_songs)) * 100, 1))) + '%]')
            try:
                delete_song = Song.objects.get(filePath=song_file_path)
                id_number = delete_song.id
                delete_song.delete()
                print('        Song "' + song_file_path + '" deleted with id: ' + str(id_number))
            except Exception as e:
                print('FAILURE - Deleting database_file. Exception: ' + str(e))
        print('        ENDING - Deleting old database entries with no file')
        return

    def get_all_paths(self, folder):
        print('        STARTING - Get file-path-tree')
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
            print(str(e))
            paths = None
        print('        ENDING - Get file-path-tree')
        return paths

    def get_list_of_all_files(self, paths, folder):
        print('        STARTING - Getting list-of-all-files')
        all_file_paths = []
        try:
            for path in paths:
                if not len(paths[path]) == 0 and path != 'meta':
                    for song_name in paths[path]:
                        all_file_paths.append((path.replace(folder, '') + '/' + song_name)[1:])
        except Exception as e:
            print(str(e))
            all_file_paths = None
        print('        ENDING - Getting list-of-all-files')
        return all_file_paths

    def get_md5_hash(self, file_path):
        md5_hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buf = file.read()
        md5_hasher.update(buf)
        file_hash = md5_hasher.hexdigest()
        return file_hash

    def get_list_of_tracked_songs(self, songs):
        list_of_tracked_songs = []
        for song in songs:
            list_of_tracked_songs.append(song.filePath)
        return list_of_tracked_songs

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
            print(str(e))
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
            print(str(e))
            id_number = None

        return id_number

    def get_dictionary_of_keywords(self, file_path):
        dictionary_of_keywords = {}
        file_opener = open(file_path, 'r')
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
