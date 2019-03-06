from bs4 import BeautifulSoup as bs
from lib.common import getContent
from lib.mongodb import operations
from lib.jobs_log import updateJobStatus
import re 

def parser(job):
    obj = operations()
    file_path = job['storage_path']
    content = getContent(file_path)
    soup = bs(content, 'html.parser')
    records = soup.find_all('article')
    for record in records:
        doctor_name = record.find('h1').text.strip()
        info = record.find('div', {'class':'art-postcontent clearfix'})
        info = '; '.join([i.text for i in info.find_all('p')])
        data = dict()
        data['job_id'] = job['job_id']
        data['doctor_name'] = doctor_name
        data['info'] = re.sub('\n+', ' ', info)
        data['file_path'] = file_path  
        data['domain'] = job['domain']
        data['url'] = job['input']['url']
        obj.insert_one('in', job['collection'], data)

    #Log to database 
    obj.closeConnection()
    job['is_parsed'] = "True"
    updateJobStatus(job['job_id'], job)
