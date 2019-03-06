from lib.mongodb import operations
from lib.config_handler import handler

obj = operations()
spot_db = handler('database','spot_db')
spot_col = handler('database', 'spot_col')

def saveJob(job):
    status = obj.insert_one(spot_db, spot_col, job)
    return status

def updateJobStatus(job_id, job):
    status = obj.update_it(spot_db, spot_col, {'job_id': job_id}, job)
    return status

def checkFile(storage_id):
    status, storage_path = obj.recordExist(spot_db, spot_col, {'storage_id': storage_id })
    return status, storage_path

def samejobCount(storage_id):
    status, records = obj.find_in_mongo(spot_db, spot_col, {'storage_id': storage_id})
    if status == True:
        records = list(records)
        return len(records)
    elif status == False:
        return 1
