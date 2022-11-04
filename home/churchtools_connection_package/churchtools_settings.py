from home.models import AdminSetting
admin_setting = AdminSetting.objects.get(id=1)
# mode can be production/testing. In testing mode the test_data have to be filled
run_mode = 'run'
test_data = [{'id': 629, 'name': 'Verbandsgottesdienst', 'date': '11.09.2022  10:30', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': 'Andreas Bietz',
              'service_predigt': 'Lisa Klotz', 'service_presentation': 'Jakob Bär'},
             {'id': 631, 'name': 'Gottesdienst mit Abendmahl', 'date': '18.09.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '',
              'service_predigt': 'Marion Bietz', 'service_presentation': 'Friederike Frech'},
             {'id': 633, 'name': 'Gottesdienst Jubiläum Posauenchor', 'date': '25.09.2022  15:00',
              'agenda_state': 'not_final', 'last_change_person': 'Andreas Bietz',
              'last_change_date': '05.08.2022  17:31', 'service_leitung': '', 'service_predigt': 'Andreas Bietz',
              'service_presentation': ''},
             {'id': 676, 'name': 'Gottesdienst', 'date': '02.10.2022  18:00', 'agenda_state': 'not_found',
              'last_change_person': '', 'last_change_date': '', 'service_leitung': '', 'service_predigt': '',
              'service_presentation': ''}]

# variable settings
song_folder = admin_setting.song_folder

powerpoint_vorlage = admin_setting.powerpoin_vorlage

# church_tools settings
serviceId_predigt = 1
serviceId_leitung = 3
serviceId_presentation = 7

base_url = admin_setting.base_url

login_token = admin_setting.login_token

fuzzy_border = 90
