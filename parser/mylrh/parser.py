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
    soup = soup.find("div",{"class":"resultsList"})
    for record in soup.find_all("div",{'itemtype':"https://schema.org/Physician"}):
        doctor_name = record.find('h1', {"itemprop":"name"}).text.strip()
        specialties = record.find('div',{'class':"specialties"}).text.strip()
        specialties = re.sub('\s+|\n+', ' ', specialties)
        data = dict()
        data['doctor_name'] = doctor_name
        data['job_id'] = job['job_id']
        data['specialties'] = specialties
        count = 1 
        for rd in record.find_all('div', {'itemprop':'address'}):
            address = rd.text.strip()
            address = re.sub('\s+|\n+',' ', address)
            data['address_%s'%count] = address
            count += 1
        obj.insert_one('in', job['collection'], data)

    #Log to database 
    obj.closeConnection()
    job['is_parsed'] = "True"
    updateJobStatus(job['job_id'], job)
