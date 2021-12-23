# mode can be production/testing. In testing mode the test_data have to be filled
run_mode = 'testing'
test_data = [{'id': 466, 'name': 'Gottesdienst', 'date': '24.12.2021  16:00', 'agenda_state': 'final',
              'last_change_person': 'Christine Fasol', 'last_change_date': '19.12.2021  20:28',
              'service_leitung': 'Team Familiengottesdienst', 'service_predigt': 'Marion Bietz',
              'service_presentation': 'Jakob Bär'},
             {'id': 469, 'name': 'Gottesdienst', 'date': '26.12.2021  18:00', 'agenda_state': 'final',
              'last_change_person': 'Marion Bietz', 'last_change_date': '22.12.2021  15:06',
              'service_leitung': 'Marion Bietz', 'service_predigt': 'Andreas Bietz',
              'service_presentation': 'Jakob Bär'},
             {'id': 472, 'name': 'Gottesdienst', 'date': '02.01.2022  18:00', 'agenda_state': 'not_final',
              'last_change_person': 'Andreas Bietz', 'last_change_date': '23.12.2021  12:42',
              'service_leitung': 'Annette Bär', 'service_predigt': 'Anja Kurt', 'service_presentation': ''},
             {'id': 475, 'name': 'Gottesdienst', 'date': '09.01.2022  18:00', 'agenda_state': 'not_final',
              'last_change_person': 'Andreas Bietz', 'last_change_date': '09.12.2021  18:19',
              'service_leitung': 'Thomas Jotter', 'service_predigt': 'Johannes Fischer',
              'service_presentation': 'Matthias Ewald'},
             {'id': 478, 'name': 'Gottesdienst', 'date': '16.01.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Marion Bietz', 'service_presentation': 'Matthias Ewald'},
             {'id': 481, 'name': 'Gottesdienst', 'date': '23.01.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Andreas Bietz', 'service_presentation': 'Matthias Ewald'},
             {'id': 484, 'name': 'Gottesdienst', 'date': '30.01.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Andreas Bietz', 'service_presentation': ''},
             {'id': 486, 'name': 'Gottesdienst', 'date': '06.02.2022  11:00', 'agenda_state': 'not_final',
              'last_change_person': 'Samuel Schlingheider', 'last_change_date': '16.11.2020  09:36',
              'service_leitung': 'Team Familiengottesdienst', 'service_predigt': 'Adonia Musical',
              'service_presentation': ''},
             {'id': 489, 'name': 'Gottesdienst', 'date': '13.02.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Amrei und Dirk Poganatz', 'service_presentation': ''},
             {'id': 492, 'name': 'Gottesdienst', 'date': '20.02.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '', 'service_predigt': '',
              'service_presentation': ''}]

# variable settings
countdown_file_path = ''

song_folder = ''

powerpoint_vorlage = ''

# normal settings
songbooks = ['FJ', 'Fj', 'CCLI', 'GLB', 'JUF']

# church_tools settings
serviceId_predigt = 1
serviceId_leitung = 3
serviceId_presentation = 7

base_url = ''

login_token = ''

login_token_url = "?login_token=" + str(login_token)

calenders = []
