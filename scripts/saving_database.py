import os
import shutil
import datetime

def print_info(info):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%d/%m/%Y_%H:%M:%S")}] {info}')

src_path = "/opt/django-apps/data/presentation_creator_website/data/"
dest_path = "/opt/django-apps/data/presentation_creator_website/backups/"

print_info('######### Starting Saving database #########')
now = datetime.datetime.now()
time_for_output_file = now.strftime('%d-%m-%Y_%H:%M')

saving_file = f'{dest_path}db_backup_{time_for_output_file}.sqlite3'
try:
    os.chdir(src_path)
    shutil.copy('db.sqlite3', saving_file)
    print(f'Saved Database in {saving_file}')
except Exception as e:
    print(f'Could not Save Database in {saving_file}. Because of: {str(e)}')

dates = os.listdir(dest_path)
dates.sort()
for date in dates:
    datum = date[10:26]
    datumtime = datetime.datetime.strptime(datum, '%d-%m-%Y_%H:%M')
    time = datetime.datetime.now()
    delta = time - datumtime
    if delta.days > 31:
        filename = dest_path + date
        try:
            os.remove(filename)
            print(f'Deleted {filename}')
        except Exception as e:
            print(f'Could not Delete saved_database {filename}. Because of: {str(e)}')
print_info('######### Finishing Saving database #########')
print()
