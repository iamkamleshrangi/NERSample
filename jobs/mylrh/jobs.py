import sys
from datetime import datetime
import copy
from lib.jobs_log import saveJob
from lib.common import getId, getguId 
from lib.rq_queue import getConnections
from bs4 import BeautifulSoup
import requests 

q = getConnections()
start_url =  'https://doctors.mylrh.org/?Index=%s'

#class="paginationBar text-right"
jobs = {'is_crawled': 'False',
        'is_parsed': 'False',
        'storage_id': '',
        'extension':'htm',
        'insert_time': datetime.utcnow(),
        'update_time': datetime.utcnow(), 
        'crawl_queue': '', 
        'parse_queue': '',
        'domain': 'mylrh.org',
        'collection' : 'mylrh', 
        'job_script':'jobs.mylrh.jobs',
        'crawl_script': 'crawler.crawl.getPage',
        'parse_script':'parser.mylrh.parser.parser', 
        'priorities': 'high',
        'storage_path': '',
        'crawl_count': 0 }

html = requests.get(start_url%1).content
soup = BeautifulSoup(html, 'html.parser')
pages = soup.find('span', {"class":"paginationBar text-right"})
page_no = [ i.text for i in soup.find_all('a') ]
page_no = [i for i in page_no if i.isdigit()]
max_page = int(max(page_no))

for i in range(1, max_page + 1):
    msg = copy.deepcopy(jobs)
    page_url = start_url%i
    msg['input'] = {'url': page_url}
    msg['job_id'] = getguId()
    q.enqueue(msg['crawl_script'], msg)
    saveJob(msg)
