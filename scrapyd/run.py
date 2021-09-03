import os
import time
import redis
import json
import requests
import pandas as pd

from progress.spinner import Spinner


PROJECT_NAME = 'hh'
SERVER = os.getenv('SCRAPY_SERVER', 'scrapyd:6800')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis-scrapy')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


def deploy():
    def job_in_process(job_id):
        response = requests.get(f'http://{SERVER}/listjobs.json?project={PROJECT_NAME}')
        running_or_pending_jobs = [
            *[i['id'] for i in response.json()['running']],
            *[i['id'] for i in response.json()['pending']]
        ]
        return job_id in running_or_pending_jobs

    keyword = os.getenv('KEYWORD', None)
    if not keyword:
        print('F**k, use Keyword env to search')
    os.system('scrapyd-deploy')
    data = {
        'project': PROJECT_NAME,
        'spider': PROJECT_NAME,
        'search': keyword
    }
    response = requests.post(f'http://{SERVER}/schedule.json', data=data)
    job_id = response.json()['jobid']

    spinner = Spinner('Parsing... ')
    while job_in_process(job_id):
        time.sleep(3)
        spinner.next()
    print('Done')


def create_df():
    reader = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        password=REDIS_PASSWORD
    )
    # that function uses reader variable
    def read_from_reader_iterator():
        cursor = '0'
        while cursor != 0:
            cursor, keys = reader.scan(cursor=cursor)
            values = reader.mget(*keys)
            values = map(json.loads, values)
            for item in values:
                yield item
    return pd.DataFrame([i for i in read_from_reader_iterator()])


def run():
    deploy()
    df = create_df()
    # Use your function there


if __name__ == "__main__":
    run()
