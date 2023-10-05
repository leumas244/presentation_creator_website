#import imp
from fuzzywuzzy import fuzz
import os
import re

from .churchtoos_api_conection import get_agenda_by_event_id, get_right_time
from .settings import fuzzy_border
from .songbeamer_file_creator import add_item_countdown, add_item_header, add_item_normal, add_item_song, add_item_state, add_item_vaterunser, create_a_new_songbeamer_file
from .powerpoint_creator import create_pp_file, set_weekvers_in_pp_by_placeholder, set_informations_in_pp_by_placeholder

from home.models import Song, AdditionalUserInfo, RenderdSongbeamerFile, Agenda, RenderdPowerpointFile


def get_event_date_from_agenda(agenda_dictionary):
    return agenda_dictionary["data"]["name"][0:10]


def get_event_name(agenda_dictionary):
    godiname = 'Gottesdienst am ' + get_event_date_from_agenda(agenda_dictionary).replace('.', '-')
    return godiname


def create_event_folder(event_folder_path):
    if not os.path.exists(event_folder_path):
        os.makedirs(event_folder_path)
    return event_folder_path


def initial_a_new_songbeamer_file(agenda_dictionary):
    event_name = get_event_name(agenda_dictionary)
    event_folder_path = f'./home/churchtools_connection_package/Gottesdienste/{event_name}' 
    event_folder = create_event_folder(event_folder_path) + '/'

    col_filename = create_a_new_songbeamer_file(event_name, event_folder)

    return col_filename


def initial_a_new_powerpoint_file(agenda_dictionary):
    event_name = get_event_name(agenda_dictionary)
    event_folder_path = f'./home/churchtools_connection_package/Gottesdienste/{event_name}' 
    event_folder = create_event_folder(event_folder_path) + '/'

    powerpoint_filename = create_pp_file(event_name, event_folder)

    return powerpoint_filename


def get_all_necessary_agenda_information(agenda_id):
    songs = Song.objects.all()
    agenda = get_agenda_by_event_id(agenda_id)
    data_dic = {"title": agenda["data"]["name"], "isFinal": agenda["data"]["isFinal"]}
    items = []
    for item in agenda["data"]["items"]:
        item_data = {
            "title": item["title"],
            "note": item["note"],
            "type": item["type"],
            "song": None,
            "time": get_right_time(item["start"]),
            "isBeforeEvent": item["isBeforeEvent"],
        }
        if item["note"]:
            if "\n-" in item["note"]:
                note = item["note"]
                note = re.sub(r'^- ', '', note)
                item_data["note"] = note.split('\n-')
            else:
                note = item["note"]
                note = re.sub(r'^- ', '', note)
                item_data["note"] = [note]

        responsible = item["responsible"]["text"]
        for person in item["responsible"]["persons"]:
            if person["accepted"]:
                if person["service"] in responsible:
                    responsible = responsible.replace(person["service"], person["person"]["title"])

        item_data["responsible"] = responsible
        items.append(item_data)

        if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
            if ":" in item['title']:
                item_data["type"] = "song"
                song = song_converter(songs, item)
                item_data["song"] = song
        elif 'musikteam' in responsible.lower():
            item_data["type"] = "song"
            song = song_converter_without_colon(songs, item)
            item_data["song"] = song

    data_dic["items"] = items

    return data_dic


def song_converter(songs, item):
        title = item['title']
        if ':' in title:
            title_split = title.split(':')
            if 'Lied' in title_split[0] or 'lied' in title_split[0]:
                if len(title_split) > 0:
                    title_without_header = title_split[1]
                    title_without_header = ''
                    for split in title_split:
                        if title_split.index(split) != 0:
                            title_without_header = title_without_header + split
                    if title_without_header == "" or title_without_header == " ":
                        return [[0, "Kein Titel"]]

                    songs_founded = search_song(songs, title_without_header)

                    fuzzy_matches_list = fuzzy_pattern(songs, title_without_header)

                    end_result = result_decider(fuzzy_matches_list, songs_founded)

                    new_end_result = get_new_end_result(end_result)
                    return new_end_result
        
            else:
                return [[0, "Problem! Kein 'Lied' in Titel gefunden!"]]
        
        else:
                return [[0, "Problem! Kein Doppelpunkt gefunden!"]]


def song_converter_without_colon(songs, item):
    title_without_header = item['title']
    songs_founded = search_song(songs, title_without_header)

    fuzzy_matches_list = fuzzy_pattern(songs, title_without_header)

    end_result = result_decider(fuzzy_matches_list, songs_founded)

    new_end_result = get_new_end_result(end_result)
    return new_end_result


def search_song(songs, title_without_header):
    songs_founded = []
    if ';' in title_without_header:
        title_without_header_split = title_without_header.split(';')
        title = title_without_header_split[0]
        if title[0] == ' ':
            title = title[1:len(title)]
        for song in songs:
            if song.title == title:
                songs_founded.append(song)
    return songs_founded


def fuzzy_pattern(songs, title):
    if title == '' or title == ' ':
        return []
    hunderter_founds = []
    border_founds = []
    selection_founds = []

    for song in songs:
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

        elif fuzzy_value_lang_1 > fuzzy_border:
            border_founds.append([fuzzy_value_lang_1, song])
        elif fuzzy_value_lang_2 > fuzzy_border:
            border_founds.append([fuzzy_value_lang_2, song])
        elif fuzzy_value_lang_3 > fuzzy_border:
            border_founds.append([fuzzy_value_lang_3, song])
        elif fuzzy_value_lang_4 > fuzzy_border:
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
        border_founds.sort(reverse=True, key=get_first_element_of_list)
        return border_founds
    else:
        selection_founds.sort(reverse=True, key=get_first_element_of_list)
        return selection_founds

def get_first_element_of_list(list):
    return list[0]
    
def result_decider(fuzzy_matches, own_matches):
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
    

def get_new_end_result(end_result):
    new_end_result = []
    for item in end_result:
        song = item[1]
        content = song.content
        content_list = content.split('---')
        content_string = ''
        for list_element in content_list:
            if not content_list.index(list_element) == 0:
                content_string = content_string + list_element
        item.append(content_string)
        new_end_result.append(item)
    return new_end_result


def create_songbeamer_file(id_number, user, songs):
    agenda = get_agenda_by_event_id(id_number)
    counter = 1

    songbeamer_file = initial_a_new_songbeamer_file(agenda)
    add_item_state(songbeamer_file, agenda['data']['isFinal'])

    add_user_info = AdditionalUserInfo.objects.get(user=user)
    countdown_path = add_user_info.countdown_file_path

    for item in agenda['data']['items']:
        if item['type'] == 'normal':
            if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
                if counter in songs:
                    if songs[counter] == 'no_song_set':
                        add_item_song(songbeamer_file, 'No song set', item['title'])
                    elif songs[counter] == 'no_file_set':
                        add_item_song(songbeamer_file, 'No File Found', item['title'])
                    else:
                        song = Song.objects.get(id=songs[counter])
                        add_item_song(songbeamer_file, song.filePath, item['title'])
            elif 'musikteam' in item["responsible"]["text"].lower():
                if counter in songs:
                    if songs[counter] == 'no_song_set':
                        add_item_song(songbeamer_file, 'No song set', item['title'])
                    elif songs[counter] == 'no_file_set':
                        add_item_song(songbeamer_file, 'No File Found', item['title'])
                    else:
                        song = Song.objects.get(id=songs[counter])
                        add_item_song(songbeamer_file, song.filePath, item['title'])
            elif 'Countdown' in item['title']:
                add_item_countdown(songbeamer_file, countdown_path)
            elif 'Vaterunser' in item['title']:
                add_item_vaterunser(songbeamer_file, item['title'])
            elif 'Besprechung' in item['title']:
                pass
            elif 'Informationen' in item['title']:
                add_item_normal(songbeamer_file, item['title'])
            else:
                add_item_normal(songbeamer_file, item['title'])

        elif item['type'] == 'header':
            add_item_header(songbeamer_file, item['title'])
        
        counter += 1
    try:
        agenda = Agenda.objects.get(church_tools_id=id_number)
        new_dataset = RenderdSongbeamerFile(user=user, agenda=agenda, songs=songs)
    except:
        new_dataset = RenderdSongbeamerFile(user=user, songs=songs)
    new_dataset.save()

    return songbeamer_file


def create_presentation_file(id_number, user):
    agenda = get_agenda_by_event_id(id_number)

    powerpoint_file = initial_a_new_powerpoint_file(agenda)

    set_weekvers_in_pp_by_placeholder(powerpoint_file, agenda)

    information_found = False
    for item in agenda['data']['items']:
        if item['type'] == 'normal':
            if not item['isBeforeEvent']:
                if 'Informationen' in item['title']:
                    set_informations_in_pp_by_placeholder(powerpoint_file, item['note'])
                    information_found = True
    
    if not information_found:
        set_informations_in_pp_by_placeholder(powerpoint_file, None)
        
    try:
        agenda = Agenda.objects.get(church_tools_id=id_number)
        new_dataset = RenderdPowerpointFile(user=user, agenda=agenda)
    except:
        new_dataset = RenderdPowerpointFile(user=user)
    new_dataset.save()

    return powerpoint_file
"""
def create_presentation(id_number, countdown_path):
    datas = get_agenda_by_event_id(id_number)

    col_filename, pptx_filename = initial_a_new_godi(datas)
    add_item_state(col_filename, datas['data']['isFinal'])
 
    set_weekvers_in_pp_by_placeholder(pptx_filename, form_godi_date(datas))

    for item in datas['data']['items']:
        if item['type'] == 'normal':
            if "Lied" in item['title'] or "lied" in item['title'] or "Song" in item['title']:
                song = get_song_from_normal_type(item['title'])
                add_item_song(col_filename, song, item['title'])
            elif 'Countdown' in item['title']:
                add_item_countdown(col_filename, countdown_path)
            elif 'Vaterunser' in item['title']:
                add_item_vaterunser(col_filename, item['title'])
            elif 'Besprechung' in item['title']:
                pass
            # elif 'Predigt:' in item['title']:
            # pass
            elif 'Informationen' in item['title']:
                set_informations_in_pp_by_placeholder(pptx_filename, item['note'])
                add_item_normal(col_filename, item['title'])
            else:
                add_item_normal(col_filename, item['title'])

        elif item['type'] == 'header':
            add_item_header(col_filename, item['title'])

        elif item['type'] == 'song':
            song = get_song_from_song_type(item['song']['title'])
            add_item_song(col_filename, song, item['song']['title'])
    return col_filename, pptx_filename
    """
