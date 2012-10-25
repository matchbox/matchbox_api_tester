api_integration_tests
=====================

integration tests that run against the api to ensure we haven't broken anything
relied upon by the backbone, ios applications, or customer integrations.

program will exit with a 0 status code if successful

currently deployed to an ec2 instance under cron

this project should be kept simple and public so other people can see how
to use the api

how to run
----------

1. update the settings.py file with your user and hostname for the service
2. install dependencies with `pip install -r requirements`
3. `python test.py`

known issues
------------

1. don't have sufficient coverage across api's
2. doesn't yet log the times for each api call for monitoring
