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

job = {'is_crawled': 'True', 'is_parsed': 'False', 'storage_id': '93ad754167138390b9ca05b7226bb94a', 
        'extension': 'htm', 'insert_time': '', 'update_time': '', 'crawl_queue': '', 'parse_queue': '', 
        'domain': 'smchealth', 'collection': 'smchealth', 'job_script': 'jobs.smchealth.jobs', 
        'crawl_script': 'crawler.crawl.getPage', 'parse_script': 'parser.smchealth.parser.parser', 
        'priorities': 'high', 
        'storage_path': '/Users/kamlesh/WorkSpace/simpleSpider/public/d818748f716a45f1889c32978a71cc5c.htm', 
        'crawl_count': 0, 
        'input': {'url': 'https://www.bethesdaweb.com/index.cfm?fuseaction=physicianlocator.main&srch_SortOptions=name&srch_ItemsPerPage=10&page=1'}, 
        'job_id': 'f9d823a7d38642f1a2ba612c5cbf50db'}

parser(job)
