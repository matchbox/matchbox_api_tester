import json
import requests
from time import time
from pprint import pprint
from settings import *

HEADERS = {'content-type': 'application/json', 'accepts': 'application/json'}


def url(location):
    return 'https://' + HOSTNAME + location


def get_programs():
    res = requests.get(url('/api/v2/program/'), headers=HEADERS, auth=AUTH)
    assert res.status_code == 200
    return res.json


def create_application(program_id, details):
    application = {
        'program_id': program_id,
        'first_name': 'Joe',
        'last_name': 'Smith',
        'external_id': int(time() * 10),
        'details': details
    }
    res = requests.post(url('/api/v2/application/'),
        headers=HEADERS, data=json.dumps(application), auth=AUTH)
    assert res.status_code == 201
    assert 'location' in res.headers
    new_application_url = res.headers.get('location')
    new_application_url = new_application_url.replace(
        url('/api/v2/application/'), '')
    return new_application_url[:-1]


def get_application(application_id):
    res = requests.get(url('/api/v2/application/%s/' % application_id),
        auth=AUTH)
    assert res.status_code == 200
    return res.json


def get_fields(program_id):
    res = requests.get(url('/api/v2/%s/application/field/' % program_id),
        headers=HEADERS, auth=AUTH)
    return res.json


def main():
    programs = get_programs().get('objects')
    assert len(programs) == 1
    program = programs[0]
    fields = get_fields(program.get('id')).get('objects')
    application_details = {}
    for f in fields:
        if 'application/field' in f.get('resource_uri'):
            application_details[f.get('reference_code')] = \
                'Testing for ' + f.get('reference_code')
    application_id = create_application(program.get('id'), application_details)
    print "new application created with id", application_id
    application = get_application(application_id)
    assert application['id'] == application_id


if __name__ == '__main__':
    main()
