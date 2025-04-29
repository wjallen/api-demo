#!/usr/bin/env python3
import logging
from jobs import q, jdb, update_job_status, results
import time
import matplotlib.pyplot as plt
import json


logging.basicConfig(level='INFO')

def plot_data(data):
    plt.bar(data.keys(), data.values(), 0.5, color='g')
    plt.xlabel('year') # Add a label to the x-axis.
    plt.ylabel('frequency') # Add a label to the y-axis.
    plt.title('Number of genes discovered per year') # Add a graph title.
    plt.savefig('/output.png')


@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    logging.info(f'starting job {jdb.get(jid)}')
    # 1 get the jobid parameters {start=1, end=5}
    # 2 go to redis, rd get data within that range
    # 3 transform into a working form
    data = { "2001": 3, "2002": 10, "2003": 6, "2004": 5}

    # 4 plot my data
    plot_data(data)

    # 5 load plot into redis
    with open('/output.png', 'rb') as f:
        img = f.read()
    results.hset(jid, 'data', json.dumps(data))
    results.hset(jid, 'image', img)       # 'results' is a client to the results db

    #time.sleep(5)
    update_job_status(jid, 'complete')
    logging.info(f'completed job {jdb.get(jid)}')

execute_job()
