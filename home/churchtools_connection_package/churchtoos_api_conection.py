import json
import requests
import datetime
import pytz

from .settings import login_token, base_url, run_mode, test_data, serviceId_leitung, serviceId_predigt, \
    serviceId_presentation


def request_to_church_tools(url):
    login_token_url = "?login_token=" + str(login_token)
    if '&' in url:
        login_token_url = login_token_url.replace('?', '')

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
    get_event_url = base_url + "events/" + str(event_id)

    data = request_to_church_tools(get_event_url)
    return data


def get_person_by_person_id(person_id):
    # build the api-url
    get_person_url = base_url + 'persons/' + str(person_id)

    data = request_to_church_tools(get_person_url)
    return data


def get_person_name_by_person_id(person_id):
    person_data = get_person_by_person_id(person_id)
    first_name = person_data['data']['firstName']
    last_name = person_data['data']['lastName']
    person_name = first_name + ' ' + last_name
    return person_name


def get_events(start=None, to=None):
    # build the api-url
    if start is None and to is None:
        get_agenda_url = base_url + "events"
    elif start is not None and to is not None:
        get_agenda_url = base_url + "events?from=" + start + '&to=' + to + "&"
    elif start is None and to is not None:
        get_agenda_url = base_url + "events?to=" + to + "&"
    else:
        get_agenda_url = base_url + "events?from=" + start + "&"

    data = request_to_church_tools(get_agenda_url)
    return data


def get_right_time(start_date):
    date_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    timezone = pytz.timezone("Europe/Berlin")
    right_time = pytz.utc.localize(date_time_obj, is_dst=None).astimezone(timezone)
    return right_time


def get_agenda_state_by_event_id(agenda_dictionary):
    if 'message' in agenda_dictionary:
        agenda_state = 'not_found'
    else:
        if agenda_dictionary['data']['isFinal']:
            agenda_state = 'final'
        else:
            agenda_state = 'not_final'
    return agenda_state


def get_service_person_by_service_id_by_event_id(event_dictionary, service_id):
    person = ''
    for eventServices in event_dictionary['data']['eventServices']:
        if eventServices['serviceId'] == service_id:
            person = eventServices['name']
            if person is None:
                person = ''
            else:
                if eventServices['agreed']:
                    return person
                else:
                    return person + '?'
    return person


def get_last_agenda_change_date_by_agenda(agenda_dictionary):
    date = agenda_dictionary['data']['meta']['modifiedDate']
    right_date = get_right_time(date)
    return right_date


def get_last_agenda_change_person_by_agenda(agenda_dictionary):
    person_id = agenda_dictionary['data']['meta']['modifiedPerson']['id']
    person_name = get_person_name_by_person_id(person_id)
    return person_name


def get_list_of_events(mode='short'):
    if run_mode == 'testing':
        event_list = test_data
    else:
        if mode == 'short':
            start = datetime.date.today()
            end = start + datetime.timedelta(days=31)
            events = get_events(start=start.strftime("%Y-%m-%d"), to=end.strftime("%Y-%m-%d"))
        else:
            events = get_events()

        events = events['data']
        event_list = []

        for event in events:
            if event['calendar']['title'] == 'Gottesdienst Grünstadt':
                event_dic = {'id': event['id'], 'name': event['name'], 'date': get_right_time(event['startDate'])}

                agenda = get_agenda_by_event_id(event['id'])
                event_data = get_event_by_event_id(event['id'])
                
                agenda_state = get_agenda_state_by_event_id(agenda)
                event_dic['agenda_state'] = agenda_state
                
                if agenda_state != 'not_found':
                    last_change_date = get_last_agenda_change_date_by_agenda(agenda)
                    last_change_person = get_last_agenda_change_person_by_agenda(agenda)
                
                else:
                    last_change_date = ''
                    last_change_person = ''

                event_dic['last_change_person'] = last_change_person
                event_dic['last_change_date'] = last_change_date

                service_leitung = get_service_person_by_service_id_by_event_id(event_data, serviceId_leitung)
                event_dic['service_leitung'] = service_leitung

                service_predigt = get_service_person_by_service_id_by_event_id(event_data, serviceId_predigt)
                event_dic['service_predigt'] = service_predigt

                service_presentation = get_service_person_by_service_id_by_event_id(event_data, serviceId_presentation)
                event_dic['service_presentation'] = service_presentation

                event_list.append(event_dic)

    return event_list
