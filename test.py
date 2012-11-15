import json
import requests
from time import time
from pprint import pprint
from settings import *

HEADERS = {'content-type': 'application/json', 'accepts': 'application/json'}


def fancy_print(line):
    print "*" * 78
    print line


def _url(location):
    return 'https://' + HOSTNAME + location


def get(location):
    res = requests.get(_url(location), headers=HEADERS, auth=AUTH)
    assert res.status_code == 200
    return res.json


def post(location, body):
    res = requests.post(_url(location),
                        headers=HEADERS,
                        data=body,
                        auth=AUTH)
    return res  # not returning json because you probably want headers


def create_application(program_id, details):
    application = {
        'program_id': program_id,
        'first_name': 'Joe',
        'last_name': 'Smith',
        'external_id': int(time() * 10),
        'details': details
    }
    res = post('/api/v2/application/', json.dumps(application))
    assert res.status_code == 201

    # will redirect you to the record you made
    assert 'location' in res.headers
    new_application_url = res.headers.get('location')
    new_application_url = new_application_url.replace(
        _url('/api/v2/application/'), '')
    return new_application_url[:-1]


def main():

    # get the program my user can see
    fancy_print("MY PROGRAMS")
    programs = get('/api/v2/program/').get('objects')
    pprint(programs)
    assert len(programs) == 1
    program = programs[0]

    # find the applicant fields available to this program
    fancy_print("FIELDS")
    fields = get('/api/v2/%s/application/field/' % program['id'])['objects']
    pprint(fields)

    # make an application with fake data in all application fields
    fancy_print("CREATING APPLICATION")
    application_details = {}
    for f in fields:
        # only set values for application fields
        if 'application/field' in f.get('resource_uri'):
            application_details[f.get('reference_code')] = \
                'Testing for ' + f.get('reference_code')
    application_id = create_application(program.get('id'), application_details)

    print "new application created with id", application_id
    application = get('/api/v2/application/%s/' % application_id)
    pprint(application)

    # what activities can I assign?
    # add ?details=ALL to the url to get more information
    activities = get('/api/v2/%s/activity/' % program['id'])['objects']
    print "*" * 80, "\n", "ACTIVITIES"
    pprint(activities)

    # what are the existing assignments that I can see?
    fancy_print("EXISTING ASSIGNMENTS")
    assignments = get('/api/v2/%s/assignment/' % program['id'])['objects']
    pprint(assignments)

    # TODO: create assignment
    # TODO: update assignment
    # TODO: query user and activity stats


if __name__ == '__main__':
    main()
