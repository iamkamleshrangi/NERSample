import sys
from datetime import datetime
import copy
from lib.jobs_log import saveJob
from lib.common import getId, getguId 
from lib.rq_queue import getConnections

q = getConnections()
start_url =  'https://treasurevalleyhospital.com/our-doctors'

jobs = {'is_crawled': 'False',
        'is_parsed': 'False',
        'storage_id': '',
        'extension':'htm',
        'insert_time': datetime.utcnow(),
        'update_time': datetime.utcnow(), 
        'crawl_queue': '', 
        'parse_queue': '',
        'domain': 'treasurevalleyhospital.com',
        'collection' : 'treasurevalleyhospital', 
        'job_script':'jobs.treasurevalleyhospital.jobs',
        'crawl_script': 'crawler.crawl.getPage',
        'parse_script':'parser.treasurevalleyhospital.parser.parser', 
        'priorities': 'high',
        'storage_path': '',
        'crawl_count': 0 }

msg = copy.deepcopy(jobs)
msg['input'] = {'url': start_url}
msg['job_id'] = getguId()
q.enqueue(msg['crawl_script'], msg)
saveJob(msg)
