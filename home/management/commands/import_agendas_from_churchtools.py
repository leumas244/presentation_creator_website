import json
import requests
import datetime
import pytz
import progressbar
import sys

from django.core.management.base import BaseCommand
from home.models import Agenda
from home.churchtools_connection_package.settings import login_token, base_url
from home.helper_package.helper_funktions import send_exeption_mail_by_automatic_script


class Command(BaseCommand):
    help = 'Import automatically agendas from ChurchTools to database'

    def handle(self, *args, **options):
        self.print_info('STARTING IMPORTING_AGENDA_FROM_CHURCHTOOLS')
        try:
            self.start_routine()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                         'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                         'lineno'  : str(exc_traceback.tb_lineno),
                         'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                         'type'    : str(exc_type.__name__),
                         'message' : str(exc_value),
                        }
            send_exeption_mail_by_automatic_script(traceback_details)
            self.print_info('ENDING IMPORTING_AGENDA_FROM_CHURCHTOOLS WITH AN ERROR: ' + str(e))
            exit()
        
        self.print_info('ENDING IMPORTING_AGENDA_FROM_CHURCHTOOLS')
        print()


    def print_info(self, info):
        now_funktion = datetime.datetime.now()
        print(f"[{now_funktion.strftime('%Y/%m/%d %H:%M:%S')}] {info}")


    def start_routine(self):
        start_date = '2020-11-01'
        tracked_events = Agenda.objects.all()
        tracked_event_ids = []

        for event in tracked_events:
            tracked_event_ids.append(event.church_tools_id)

        all_events = self.get_all_events(start_date)
        
        counter_all = 0
        for event in all_events:
            if event['calendar']['title'] == 'Gottesdienst Grünstadt':
                counter_all += 1

        bar = progressbar.ProgressBar(maxval=counter_all, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        counter_done = 0
        counter_updated = 0
        counter_not_updated = 0
        counter_created = 0
        counter_event_without_agenda = 0
        counter_deleted_event = 0
        for event in all_events:
            if event['calendar']['title'] == 'Gottesdienst Grünstadt':
                if event['id'] in tracked_event_ids:
                    tracked_event_ids.remove(event['id'])
                    agenda = self.get_agenda_by_event_id(event['id'])
                    tracked_agenda = Agenda.objects.get(church_tools_id=event['id'])
                    agenda_state = self.get_agenda_state_agenda_dictonary(agenda)
                    if agenda_state:
                        if agenda == json.loads(tracked_agenda.content):
                            counter_not_updated += 1
                        else:
                            try:
                                tracked_agenda.content = json.dumps(agenda)
                                tracked_agenda.agenda_state = agenda_state
                                tracked_agenda.save()
                                counter_updated += 1
                            except Exception as e:
                                exc_type, exc_value, exc_traceback = sys.exc_info()
                                traceback_details = {'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                                                    'lineno'  : str(exc_traceback.tb_lineno),
                                                    'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                                                    'type'    : str(exc_type.__name__),
                                                    'message' : str(exc_value),
                                                    }
                                send_exeption_mail_by_automatic_script(traceback_details)
                                print(f'Could not create new Agenda. Because of: {str(e)}')
                                print(f'Could not update Agenda with DB-ID: {tracked_agenda.id} and CT_ID: {tracked_agenda.church_tools_id}. Because of: {str(e)}')
                    else:
                        counter_event_without_agenda += 1
                else:
                    agenda = self.get_agenda_by_event_id(event['id'])
                    agenda_state = self.get_agenda_state_agenda_dictonary(agenda)
                    try:
                        new_agenda = Agenda(church_tools_id=event['id'], title=event['name'],
                                            date=self.get_right_time(event['startDate']), agenda_state=agenda_state)
                        if agenda_state:
                            new_agenda.content = json.dumps(agenda)
                        else:
                            new_agenda.content = '{"data":""}'
                        new_agenda.save()
                        counter_created += 1
                    except Exception as e:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback_details = {'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                                            'lineno'  : str(exc_traceback.tb_lineno),
                                            'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                                            'type'    : str(exc_type.__name__),
                                            'message' : str(exc_value),
                                            }
                        send_exeption_mail_by_automatic_script(traceback_details)
                        print(f'Could not create new Agenda. Because of: {str(e)}')

                bar.update(counter_done)
                counter_done += 1

        for ct_id in tracked_event_ids:
            counter_deleted_event += 1
            Agenda.objects.get(church_tools_id=ct_id).delete()
            bar.update(counter_done)
            counter_done += 1
            
        bar.finish()

        print('SUMMARY')
        print('{:<12} {:<12} {:<12} {:<12} {:<12} {:<14}'.format('Events', 'AG Created', 'AG Edit', 'AG No Edit', 'without AG', 'deleted Events'))
        print('-'*75)
        print('{:<12} {:<12} {:<12} {:<12} {:<12} {:<14}'.format(counter_all, counter_created, counter_updated, counter_not_updated, counter_event_without_agenda, counter_deleted_event))


    def request_to_church_tools(self, url):
        login_token_url = 'login_token=' + login_token
        try:
            response = requests.get(base_url + url + login_token_url)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                         'filename': str(exc_traceback.tb_frame.f_code.co_filename),
                         'lineno'  : str(exc_traceback.tb_lineno),
                         'name'    : str(exc_traceback.tb_frame.f_code.co_name),
                         'type'    : str(exc_type.__name__),
                         'message' : str(exc_value),
                        }
            send_exeption_mail_by_automatic_script(traceback_details)
            self.print_info('ENDING IMPORTING_AGENDA_FROM_CHURCHTOOLS WITH AN ERROR: ' + str(e))
            exit()

        data = json.loads(response.text)
        return data


    def get_agenda_by_event_id(self, event_id):
        get_agenda_url = "events/" + str(event_id) + "/agenda?"

        data = self.request_to_church_tools(get_agenda_url)
        return data


    def get_event_by_event_id(self, event_id):
        get_event_url = "events/" + str(event_id) + '&'

        data = self.request_to_church_tools(get_event_url)
        return data


    def get_all_events(self, start_date):
        get_agenda_url = f'events?from={start_date}&'

        data = self.request_to_church_tools(get_agenda_url)
        return data['data']


    def get_right_time(self, datetime_str):
        date_time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        timezone = pytz.timezone("Europe/Berlin")
        right_time = pytz.utc.localize(date_time_obj, is_dst=None).astimezone(timezone)
        return right_time


    def get_agenda_state_agenda_dictonary(self, agenda_dictionary):
        if 'message' in agenda_dictionary:
            agenda_state = False
        else:
            agenda_state = True
        return agenda_state
