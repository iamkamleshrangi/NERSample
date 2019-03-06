import sys
from datetime import datetime
import copy
from lib.jobs_log import saveJob
from lib.common import getId, getguId 
from lib.rq_queue import getConnections

q = getConnections()
start_url =  'https://www.smchealth.org/smmc-find-doctor?page=%s'
page_starts_at = 0
page_ends_at = 17 #Define number of pages 

jobs = {'is_crawled': 'False',
        'is_parsed': 'False',
        'storage_id': '',
        'extension':'htm',
        'insert_time': datetime.utcnow(),
        'update_time': datetime.utcnow(), 
        'crawl_queue': '', 
        'parse_queue': '',
        'domain': 'smchealth.com',
        'collection' : 'smchealth', 
        'job_script':'jobs.smchealth.jobs',
        'crawl_script': 'crawler.crawl.getPage',
        'parse_script':'parser.smchealth.parser.parser', 
        'priorities': 'high',
        'storage_path': '',
        'crawl_count': 0 }

for i in range(page_starts_at, page_ends_at+1):
    page_url = start_url%(i)
    msg = copy.deepcopy(jobs)
    msg['input'] = {'url': page_url}
    msg['job_id'] = getguId()
    q.enqueue(msg['crawl_script'], msg)
    saveJob(msg)
