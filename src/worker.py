#!/usr/bin/env python3
import logging
from jobs import q, jdb, update_job_status
import time

logging.basicConfig(level='INFO')

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    logging.info(f'starting job {jdb.get(jid)}')
    time.sleep(5)
    update_job_status(jid, 'complete')
    logging.info(f'completed job {jdb.get(jid)}')

execute_job()
