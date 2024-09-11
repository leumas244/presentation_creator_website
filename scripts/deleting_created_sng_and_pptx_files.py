import os
import shutil
import datetime

def print_info(info):
    now = datetime.datetime.now()
    print(f'[{now.strftime("%d/%m/%Y_%H:%M:%S")}] {info}')

src_path = "/opt/django-apps/data/presentation_creator_website/data/Gottesdienste/"

print_info('######### STARTING deleting_created_sng_and_pptx_files #########')

dates = os.listdir(src_path)
dates.sort()
for date in dates:
    filename = src_path + date
    try:
        shutil.rmtree(filename)
        print(f'Deleting folder {date}')
    except Exception as e:
        print(f'Could not delete {filename}. Because of: {str(e)}')

print_info('######### FINISHING deleting_created_sng_and_pptx_files #########')
print()
