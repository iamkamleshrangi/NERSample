from datetime import datetime
import copy, requests
from lib.jobs_log import saveJob
from lib.common import getId, getguId 
from lib.rq_queue import getConnections
from bs4 import BeautifulSoup

q = getConnections()
start_url =  'https://wmhweb.com/medical-staff'
urls_arr = []

jobs = {'is_crawled': 'False',
        'is_parsed': 'False',
        'storage_id': '',
        'extension':'htm',
        'insert_time': datetime.utcnow(),
        'update_time': datetime.utcnow(), 
        'crawl_queue': '', 
        'parse_queue': '',
        'domain': 'wmhweb.com',
        'collection' : 'wmhweb', 
        'job_script':'jobs.wmhweb.jobs',
        'crawl_script': 'crawler.crawl.getPage',
        'parse_script':'parser.wmhweb.parser.parser', 
        'priorities': 'high',
        'storage_path': '',
        'crawl_count': 0 }

#Auto Pages 
html = requests.get(start_url).content 
soup = BeautifulSoup(html, 'html.parser')
soup = soup.find("div", {"class":"art-pager"})
page_no = [ i.text for i in soup.find_all('a') ]
page_no = [i for i in page_no if i.isdigit()]
max_page = max(page_no)
urls_arr.append(start_url)

for number in range(2, int(max_page) + 1):
    url = 'https://wmhweb.com/medical-staff/page/%s/'%number
    urls_arr.append(url)

for page_url in urls_arr:
    msg = copy.deepcopy(jobs)
    msg['input'] = {'url': page_url}
    msg['job_id'] = getguId()
    q.enqueue(msg['crawl_script'], msg)
    saveJob(msg)
