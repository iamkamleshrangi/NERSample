import requests #ADD PROXIES 
from lib.jobs_log import updateJobStatus, checkFile, samejobCount
from lib.common import getId, savePage
from lib.rq_queue import getConnections

def getPage(job):
    job_id = job['job_id']
    q = getConnections()
    try:
        url = job['input']['url']
        page = requests.get(url)
        if page.status_code == 200:
            html_content = page.content
            storage_id = getId(html_content)
            status, storage_path = checkFile(storage_id)
            if status == False:
                file_path = savePage(html_content)
                job['storage_path'] = file_path
            elif status == True:
                job['storage_path'] = storage_path
            job['storage_id'] = storage_id
            job['is_crawled'] = "True"
            count = samejobCount(storage_id)
            job['crawl_count'] = count
            result = q.enqueue(job['parse_script'], job)
            updateJobStatus(job_id, job)
        else:
            print('Already Crawled the page')
    except Exception as e:
        print(e)
        job['errors'] = e
        updateJobStatus(job_id, job)
