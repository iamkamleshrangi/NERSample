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
    records = soup.body 

    for record in records.find_all("div",{"class":"box-content"}):
        doctor_name = record.find('h3').text
        filed_of_area = record.find('h5').text
        address = ' '.join([i.text for i in record.find_all('p')])
        data = dict()
        data['job_id'] = job['job_id']
        data['doctor_name'] = doctor_name
        data['specialty'] = filed_of_area
        data['address'] = address
        obj.insert_one('in', job['collection'], data)

    #Log to database 
    obj.closeConnection()
    job['is_parsed'] = "True"
    updateJobStatus(job['job_id'], job)
