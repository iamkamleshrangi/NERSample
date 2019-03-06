import pymongo
from lib.config_handler import handler
from pymongo import MongoClient

class operations():
    #Set Database Connection
    def __init__(self):
        host = handler('database','host')
        port = handler('database','port')
        self.conn = MongoClient(host, port)
    #Sinlge insert into the database, inserted return true else false
    def insert_one(self,dbname,colname,data):
        try:
            db = self.conn[dbname]
            col = db[colname]
            col.insert(data)
            return True 
        except:
            return False
    #Find Data Into The Collection
    def find_data(self, dbname, colname):
        try:
            db = self.conn[dbname]
            col = db[colname]
            records = col.find()
            return records
        except:
            return {}
    #Insert an array of records, inserted return true else false 
    def bulk_insert(self,dbname,colname,data_array):
        try:
            db = self.conn[dbname]
            col = db[colname]
            col.insert_many(data_array)
            return True 
        except:
            return False
    #Find query of mongodb return an json
    def find_in_mongo(self,dbname,colname,condition):
        try:
            db = self.conn[dbname]
            col = db[colname]
            records = col.find(condition)
            return True, records 
        except:
            return False, {}
    #Update database with json condition
    def update_to_mongo(self,dbname,colname,condition,data):
        try:
            db = self.conn[dbname]
            col = db[colname]
            col.update(condition,{"$set":data},upsert=True)
            return True 
        except Exception as e:
            print(e)
            return False
    #Single record update
    def update_it(self, dbname, colname, condition, data):
        try:
            db = self.conn[dbname]
            col = db[colname]
            col.update(condition, {"$set":data})
            return True
        except:
            return False
    #Check record in the database
    def recordExist(self, dbname, colname, condition):
        try:
            db = self.conn[dbname]
            col = db[colname]
            record_ids = list(col.find(condition, {'storage_path': 1 }))
            if len(record_ids) == 0:
                return False, None
            else:
                storage_path = record_ids[0]['storage_path']
                return True, storage_path
        except Exception as e:
            print(e)
            return False, None
    #Close Connection
    def closeConnection(self):
        self.conn.close()
