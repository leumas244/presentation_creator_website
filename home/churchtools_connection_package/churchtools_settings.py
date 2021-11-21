# mode can be production/testing. In testing mode the test_data have to be filled
run_mode = 'production'
test_data = [{'id': 451, 'name': 'Gottesdienst', 'date': '2021.11.21 18:00', 'agenda_state': 'not_final',
              'service_leitung': 'Sabine Riesterer', 'service_predigt': 'Andreas Bietz'},
             {'id': 454, 'name': 'Gottesdienst', 'date': '2021.11.28 11:00', 'agenda_state': 'not_final',
              'service_leitung': 'Team Familiengottesdienst', 'service_predigt': 'Andreas Bietz'},
             {'id': 457, 'name': 'Gottesdienst', 'date': '2021.12.05 18:00', 'agenda_state': 'not_found',
              'service_leitung': 'Andreas Bietz', 'service_predigt': 'Marion Bietz'},
             {'id': 460, 'name': 'Gottesdienst', 'date': '2021.12.12 18:00', 'agenda_state': 'not_found',
              'service_leitung': 'Thomas Jotter', 'service_predigt': 'Andreas Bietz'},
             {'id': 463, 'name': 'Gottesdienst', 'date': '2021.12.19 18:00', 'agenda_state': 'not_found',
              'service_leitung': 'Marion Bietz', 'service_predigt': 'Joachim Stroppel'},
             {'id': 466, 'name': 'Gottesdienst', 'date': '2021.12.24 16:00', 'agenda_state': 'not_found',
              'service_leitung': 'Team Familiengottesdienst', 'service_predigt': 'Andreas Bietz'},
             {'id': 469, 'name': 'Gottesdienst', 'date': '2021.12.26 18:00', 'agenda_state': 'not_found',
              'service_leitung': '', 'service_predigt': 'Andreas Bietz'},
             {'id': 472, 'name': 'Gottesdienst', 'date': '2022.01.02 18:00', 'agenda_state': 'not_found',
              'service_leitung': '', 'service_predigt': 'Anja Kurt'},
             {'id': 475, 'name': 'Gottesdienst', 'date': '2022.01.09 18:00', 'agenda_state': 'not_found',
              'service_leitung': '', 'service_predigt': 'Andreas Bietz'},
             {'id': 478, 'name': 'Gottesdienst', 'date': '2022.01.16 18:00', 'agenda_state': 'not_found',
              'service_leitung': '', 'service_predigt': 'Marion Bietz'}]

# variable settings
countdown_file_path = ''

song_folder = ''

powerpoint_vorlage = ''

# normal settings
songbooks = ['FJ', 'Fj', 'CCLI', 'GLB', 'JUF']

# church_tools settings
serviceId_predigt = 1
serviceId_leitung = 3

base_url = ''

login_token = ''

login_token_url = "?login_token=" + str(login_token)

calenders = ['./agenda_conv_website/ChurchTools_conv_package/data/daskirchenjahr_2019-2020.ics',
             './agenda_conv_website/ChurchTools_conv_package/data/daskirchenjahr_2020-2021.ics',
             './agenda_conv_website/ChurchTools_conv_package/data/daskirchenjahr_2021-2022.ics',
             './agenda_conv_website/ChurchTools_conv_package/data/daskirchenjahr_2022-2023.ics'
             ]
