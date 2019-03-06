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
    records = soup.find_all('div',{"class":"view-content"})[3]
    for record in records.find_all('article'):
        data = dict()
        data['job_id'] = job['job_id']
        data['file_path'] = file_path
        data['domain'] = job['collection']
        data['url'] = job['input']['url']
        data['doctor_name'] = record.find('span',{"class":"title"}).text.strip()
        info = record.find('p')
        info = str(info).replace('/','')
        info = re.sub('\<p\>|\<strong\>','', info)
        for record in info.split('<br>'):
            key = record.split(':')[0].lower()
            value = record.split(':')[1]
            value = value.replace('\xa0','')
            data[key] = value

        #Collection Insert
        obj.insert_one('in', job['collection'], data)

    #Log to database 
    obj.closeConnection()
    job['is_parsed'] = "True"
    updateJobStatus(job['job_id'], job)
