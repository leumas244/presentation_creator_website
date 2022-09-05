from .churchtoos_api_conection import get_agenda_by_event_id


def get_event_date_from_agenda(agenda_dictionary):
    return agenda_dictionary['data']['name'][0:10]


def get_all_necessary_agenda_information(agenda_id):
    pass


'''
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
    return col_filename, pptx_filename '''
