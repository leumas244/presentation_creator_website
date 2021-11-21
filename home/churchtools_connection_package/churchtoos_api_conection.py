import json
import requests
import datetime
import pytz

from .churchtools_settings import login_token_url, base_url, run_mode, test_data, serviceId_leitung, serviceId_predigt


def request_to_church_tools(url):
    response = requests.get(url + login_token_url)

    # form into dictionary
    data = json.loads(response.text)
    return data


def get_agenda_by_event_id(event_id):
    # build the api-url
    get_agenda_url = base_url + "events/" + str(
        event_id) + "/agenda"

    data = request_to_church_tools(get_agenda_url)
    return data


def get_event_by_event_id(event_id):
    # build the api-url
    get_agenda_url = base_url + "events/" + str(event_id)

    data = request_to_church_tools(get_agenda_url)
    return data


def get_events(start=None, to=None):
    # build the api-url
    if start is None and to is None:
        get_agenda_url = base_url + "events"
    elif start is not None and to is not None:
        get_agenda_url = base_url + "events?from=" + start + '&to=' + to
    elif start is None and to is not None:
        get_agenda_url = base_url + "events?to=" + to
    else:
        get_agenda_url = base_url + "events?from=" + start

    data = request_to_church_tools(get_agenda_url)
    return data


def get_right_time(start_date):
    date_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    timezone = pytz.timezone("Europe/Berlin")
    right_time = pytz.utc.localize(date_time_obj, is_dst=None).astimezone(timezone).strftime('%Y.%m.%d %H:%M')
    return right_time


def get_agenda_state_by_event_id(event_id):
    response = get_agenda_by_event_id(event_id)
    if 'message' in response:
        agenda_state = 'not_found'
    else:
        if response['data']['isFinal'] != True:
            agenda_state = 'not_final'
        else:
            agenda_state = 'final'
    return agenda_state


def get_service_person_by_service_id_by_event_id(event_id, service_id):
    response = get_event_by_event_id(event_id)
    person = ''
    for eventServices in response['data']['eventServices']:
        if eventServices['serviceId'] == service_id:
            person = eventServices['name']
            if person is None:
                person = ''
    return person


def get_list_of_events():
    if run_mode == 'testing':
        event_list = test_data
    else:
        events = get_events()

        events = events['data']
        event_list = []

        for event in events:
            if event['calendar']['title'] == 'Gottesdienst Grünstadt':
                event_dic = {'id': event['id'], 'name': event['name'], 'date': get_right_time(event['startDate'])}

                agenda_state = get_agenda_state_by_event_id(event['id'])
                event_dic['agenda_state'] = agenda_state

                service_leitung = get_service_person_by_service_id_by_event_id(event['id'], serviceId_leitung)
                event_dic['service_leitung'] = service_leitung

                service_predigt = get_service_person_by_service_id_by_event_id(event['id'], serviceId_predigt)
                event_dic['service_predigt'] = service_predigt

                event_list.append(event_dic)

    return event_list
