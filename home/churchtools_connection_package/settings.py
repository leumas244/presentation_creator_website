from home.models import AdminSetting
try:
    admin_setting = AdminSetting.objects.get(id=1)
except:
    admin_setting = None
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
if admin_setting:
    song_folder = admin_setting.song_folder
else:
    song_folder = ''

if admin_setting:
    powerpoint_vorlage = admin_setting.powerpoin_vorlage
else:
    powerpoint_vorlage = ''

# church_tools settings
serviceId_predigt = 1
serviceId_leitung = 3
serviceId_presentation = 7

if admin_setting:
    base_url = admin_setting.base_url
else:
    base_url = ''

if admin_setting:
    login_token = admin_setting.login_token
else:
    login_token = ''

fuzzy_border = 90

# book names for weekmotto and ibibles.net
ibibles_basic_url = 'http://ibibles.net/quote.php?'

html_tables_with_weekmottos = ['home/churchtools_connection_package/data/jahr_2021-2022.html',
                               'home/churchtools_connection_package/data/jahr_2022-2023.html',
                               'home/churchtools_connection_package/data/jahr_2023-2024.html',
                               'home/churchtools_connection_package/data/jahr_2024-2025.html'
                               ]

books = {'Genesis': 'ge',
        '1. Mose': 'ge',
        'Exodus': 'exo',
        '2. Mose': 'exo',
        'Levitikus': 'lev',
        '3.Mose': 'lev',
        'Numeri': 'num',
        '4. Mose': 'num',
        'Deuteronomium': 'deu',
        '5. Mose': 'deu',
        'Josua': 'josh',
        'Richter': 'jdgs',
        'Ruth': 'ruth',
        '1. Samuel': '1sm',
        '2. Samuel': '2sm',
        '1. Könige': '1ki',
        '2. Könige': '2ki',
        '1. Chronik': '1chr',
        '2. Chronik': '2chr',
        'Esra': 'ezra',
        'Nehemia': 'neh',
        'Ester': 'est',
        'Hiob': 'job',
        'Psalm': 'psa',
        'Sprüche': 'prv',
        'Prediger': 'eccl',
        'Hohelied': 'ssol',
        'Jesaja': 'isa',
        'Jeremia': 'jer',
        'Klagelieder': 'lam',
        'Hesekiel': 'eze',
        'Daniel': 'dan',
        'Hosea': 'hos',
        'Joel': 'joel',
        'Amos': 'amos',
        'Obadja': 'obad',
        'Jona': 'jonah',
        'Micha': 'mic',
        'Nahum': 'nahum',
        'Habakuk': 'hab',
        'Zefanja': 'zep',
        'Haggai': 'hag',
        'Sacharja': 'zec',
        'Maleachi': 'mal',
        'Matthäus': 'mat',
        'Mt': 'mat',
        'Markus': 'mark',
        'Mk': 'mark',
        'Lukas': 'luke',
        'Lk': 'luke',
        'Johannes': 'john',
        'Apostelgeschichte': 'acts',
        'Apg': 'acts',
        'Römer': 'rom',
        '1. Korinther': '1cor',
        '2. Korinther': '2cor',
        'Galater': 'gal',
        'Epheser': 'eph',
        'Philipper': 'phi',
        'Kolosser': 'col',
        '1. Thessalonicher': '1th',
        '2. Thessalonicher': '2th',
        '1. Timotheus': '1tim',
        '2. Timotheus': '2tim',
        'Titus': 'titus',
        'Philemon': 'phmn',
        'Hebräer': 'heb',
        'Jakobus': 'jas',
        '1. Petrus': '1pet',
        '2. Petrus': '2pet',
        '1. Johannes': '1jn',
        '2. Johannes': '2jn',
        '3. Johannes': '3jn',
        'Judas': 'jude',
        'Offenbarung': 'rev',
        'Offb': 'rev',
        }

booknames = {'Genesis': '1. Mose',
            '1. Mose': '1. Mose',
            'Exodus': '2. Mose',
            '2. Mose': '2. Mose',
            'Levitikus': '3. Mose',
            '3. Mose': '3. Mose',
            'Numeri': '4. Mose',
            '4. Mose': '4. Mose',
            'Deuteronomium': '5. Mose',
            '5. Mose': '5. Mose',
            'Josua': 'Josua',
            'Richter': 'Richter',
            'Ruth': 'Ruth',
            '1. Samuel': '1. Samuel',
            '2. Samuel': '2. Samuel',
            '1. Könige': '1. Könige',
            '2. Könige': '2. Könige',
            '1. Chronik': '1. Chronik',
            '2. Chronik': '2. Chronik',
            'Esra': 'Esra',
            'Nehemia': 'Nehemia',
            'Ester': 'Ester',
            'Hiob': 'Hiob',
            'Psalm': 'Psalm',
            'Sprüche': 'Sprüche',
            'Prediger': 'Prediger',
            'Hohelied': 'Hohelied',
            'Jesaja': 'Jesaja',
            'Jeremia': 'Jeremia',
            'Klagelieder': 'Klagelieder',
            'Hesekiel': 'Hesekiel',
            'Daniel': 'Daniel',
            'Hosea': 'Hosea',
            'Joel': 'Joel',
            'Amos': 'Amos',
            'Obadja': 'Obadja',
            'Jona': 'Jona',
            'Micha': 'Micha',
            'Nahum': 'Nahum',
            'Habakuk': 'Habakuk',
            'Zefanja': 'Zefanja',
            'Haggai': 'Haggai',
            'Sacharja': 'Sacharja',
            'Maleachi': 'Maleachi',
            'Matthäus': 'Matthäus',
            'Mt': 'Matthäus',
            'Markus': 'Markus',
            'Mk': 'Markus',
            'Lukas': 'Lukas',
            'Lk': 'Lukas',
            'Johannes': 'Johannes',
            'Apostelgeschichte': 'Apostelgeschichte',
            'Apg': 'Apostelgeschichte',
            'Römer': 'Römer',
            '1. Korinther': '1. Korinther',
            '2. Korinther': '2. Korinther',
            'Galater': 'Galater',
            'Epheser': 'Epheser',
            'Philipper': 'Philipper',
            'Kolosser': 'Kolosser',
            '1. Thessalonicher': '1. Thessalonicher',
            '2. Thessalonicher': '2. Thessalonicher',
            '1. Timotheus': '1. Timotheus',
            '2. Timotheus': '2. Timotheus',
            'Titus': 'Titus',
            'Philemon': 'Philemon',
            'Hebräer': 'Hebräer',
            'Jakobus': 'Jakobus',
            '1. Petrus': '1. Petrus',
            '2. Petrus': '2. Petrus',
            '1. Johannes': '1. Johannes',
            '2. Johannes': '2. Johannes',
            '3. Johannes': '3. Johannes',
            'Judas': 'Judas',
            'Offenbarung': 'Offenbarung',
            'Offb': 'Offenbarung',
            }