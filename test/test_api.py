#!/usr/bin/python3

import json
import os
import re
import time

import pytest
import requests


api_host = 'localhost'
api_port = '5000'
api_prefix = f'http://{api_host}:{api_port}'



def test_help_info():
    route = f'{api_prefix}/help'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert bool(re.search('To submit a job,', response.text)) == True


def test_get_jobs():
    route = f'{api_prefix}/jobs'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_jobs_cycle():
    route = f'{api_prefix}/jobs'
    job_data = {'start': 1, 'end': 2}
    response = requests.post(route, json=job_data)

    assert response.ok == True
    assert response.status_code == 200

    UUID = response.json()['id']
    assert isinstance(UUID, str) == True
    assert response.json()['status'] == 'submitted'
    assert int(response.json()['start']) == int(job_data['start'])
    assert int(response.json()['end']) == int(job_data['end'])


    time.sleep(2)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert response.json()['status'] == 'in progress'
    assert int(response.json()['start']) == int(job_data['start'])
    assert int(response.json()['end']) == int(job_data['end'])


    time.sleep(20)
    route = f'{api_prefix}/jobs/{UUID}'
    response = requests.get(route)

    assert response.ok == True
    assert response.status_code == 200

    assert response.json()['status'] == 'complete'
    assert int(response.json()['start']) == int(job_data['start'])
    assert int(response.json()['end']) == int(job_data['end'])

