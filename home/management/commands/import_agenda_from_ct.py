import json
import requests
import datetime
import pytz

from django.core.management.base import BaseCommand
from home.models import Agenda


class Command(BaseCommand):
    help = 'Import automatically agendas from CT to database'

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        print('[' + str(now) + ']')
        start_date = '2020-11-01'
        tracked_events = Agenda.objects.all()
        tracked_event_ids = []
        for event in tracked_events:
            tracked_event_ids.append(event.church_tools_id)
        all_events = self.get_events(start_date)
        all_events = all_events['data']
        counter_all = 0
        for event in all_events:
            if event['calendar']['title'] == 'Gottesdienst Grünstadt':
                counter_all = counter_all + 1
        counter_done = 0
        for event in all_events:
            if event['calendar']['title'] == 'Gottesdienst Grünstadt':
                counter_done = counter_done + 1
                print('[' + str((round((counter_done / counter_all) * 100, 1))) + '%]')
                if event['id'] in tracked_event_ids:
                    agenda = self.get_agenda_by_event_id(event['id'])
                    tracked_agenda = Agenda.objects.get(church_tools_id=event['id'])
                    agenda_state = self.get_agenda_state_by_event_id(agenda)
                    if agenda_state:
                        if agenda == json.loads(tracked_agenda.content):
                            print(str(tracked_agenda.church_tools_id) + ' has no update!')
                        else:
                            print(str(tracked_agenda.church_tools_id) + ' has an updated!')
                            try:
                                tracked_agenda.content = json.dumps(agenda)
                                tracked_agenda.agenda_state = agenda_state
                                tracked_agenda.save()
                                print(str(tracked_agenda.church_tools_id) + ' have been updated!')
                            except Exception as e:
                                print(str(tracked_agenda.church_tools_id) + ' could not be updated! Because of: ' + str(
                                    e))
                    else:
                        pass
                else:
                    agenda = self.get_agenda_by_event_id(event['id'])
                    agenda_state = self.get_agenda_state_by_event_id(agenda)
                    try:
                        new_agenda = Agenda(church_tools_id=event['id'], title=event['name'],
                                            date=self.get_right_time(event['startDate']), agenda_state=agenda_state)
                        if agenda_state:
                            new_agenda.content = json.dumps(agenda)
                        new_agenda.save()
                        print(str(new_agenda.church_tools_id) + ' has been created!')
                    except Exception as e:
                        print(str(e))
        now = datetime.datetime.now()
        print('[' + str(now) + ']')
        return

    def request_to_church_tools(self, url):
        base_url = 'https://stamigruenstadt.church.tools/api/'
        login_token = 'BWZvOMVP8tZeFA5IrfIvKkmazRrWVlHazL80H9XOazrxBhfctpONbFYKawRiHIPcs5BSHmlAwoARkrrKZR0iVjqgk46jtDnHQLBETZgRWu0PaTf7N7ToYqL7yYUXTfrCo9W7ESQleEoO4MXuOcQ3LWL95qDbS9OmykA4jGyEBhMKDNH9sTBN9VLmTLi5uJBBrAmaqLT6kScVEvzCS8NYL8MTkxSPtm8Ve6G95osEq7aJmy3CgnGxdSJDWSiFicsv'
        login_token_url = 'login_token=' + login_token

        response = requests.get(base_url + url + login_token_url)

        # form into dictionary
        data = json.loads(response.text)
        return data

    def get_agenda_by_event_id(self, event_id):
        # build the api-url
        get_agenda_url = "events/" + str(
            event_id) + "/agenda?"

        data = self.request_to_church_tools(get_agenda_url)
        return data

    def get_event_by_event_id(self, event_id):
        # build the api-url
        get_event_url = "events/" + str(event_id) + '&'

        data = self.request_to_church_tools(get_event_url)
        return data

    def get_events(self, start=None, to=None):
        # build the api-url
        if start is None and to is None:
            get_agenda_url = "events?"
        elif start is not None and to is not None:
            get_agenda_url = "events?from=" + start + '&to=' + to + '&'
        elif start is None and to is not None:
            get_agenda_url = "events?to=" + to + '&'
        else:
            get_agenda_url = "events?from=" + start + '&'

        data = self.request_to_church_tools(get_agenda_url)
        return data

    def get_right_time(self, start_date):
        date_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
        timezone = pytz.timezone("Europe/Berlin")
        right_time = pytz.utc.localize(date_time_obj, is_dst=None).astimezone(timezone)
        return right_time

    def get_agenda_state_by_event_id(self, agenda_dictionary):
        if 'message' in agenda_dictionary:
            agenda_state = False
        else:
            agenda_state = True
        return agenda_state
