# mode can be production/testing. In testing mode the test_data have to be filled
run_mode = 'testing'
test_data = [{'id': 454, 'name': 'Gottesdienst', 'date': '28.11.2021  11:00', 'agenda_state': 'not_final',
              'last_change_person': 'Andreas Bietz', 'last_change_date': '10.11.2021  11:03',
              'service_leitung': 'Team Familiengottesdienst', 'service_predigt': 'Andreas Bietz',
              'service_presentation': 'Jakob Bär'},
             {'id': 457, 'name': 'Gottesdienst', 'date': '05.12.2021  18:00', 'agenda_state': 'not_final',
              'last_change_person': 'Andreas Bietz', 'last_change_date': '25.11.2021  14:36',
              'service_leitung': 'Andreas Bietz', 'service_predigt': 'Marion Bietz', 'service_presentation': ''},
             {'id': 460, 'name': 'Gottesdienst', 'date': '12.12.2021  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': 'Thomas Jotter',
              'service_predigt': 'Andreas Bietz', 'service_presentation': ''},
             {'id': 463, 'name': 'Gottesdienst', 'date': '19.12.2021  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': 'Marion Bietz',
              'service_predigt': 'Joachim Stroppel', 'service_presentation': ''},
             {'id': 466, 'name': 'Gottesdienst', 'date': '24.12.2021  16:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': 'Team Familiengottesdienst',
              'service_predigt': 'Marion Bietz', 'service_presentation': ''},
             {'id': 469, 'name': 'Gottesdienst', 'date': '26.12.2021  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Andreas Bietz', 'service_presentation': ''},
             {'id': 472, 'name': 'Gottesdienst', 'date': '02.01.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '', 'service_predigt': 'Anja Kurt',
              'service_presentation': ''},
             {'id': 475, 'name': 'Gottesdienst', 'date': '09.01.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Andreas Bietz', 'service_presentation': ''},
             {'id': 478, 'name': 'Gottesdienst', 'date': '16.01.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Marion Bietz', 'service_presentation': ''},
             {'id': 481, 'name': 'Gottesdienst', 'date': '23.01.2022  18:00', 'agenda_state': 'not_found',
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
