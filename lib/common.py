import hashlib
import uuid
from lib.config_handler import handler
import os 

def getId(content):
   content_id = hashlib.md5(content)
   return content_id.hexdigest()

def getguId():
    guid = uuid.uuid4().hex
    return guid

def getContent(file_path):
    handler = open(file_path, 'rb')
    content = handler.read()
    handler.close()
    return content 

def savePage(content):
    dir_path = handler('settings','public_path')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_name = uuid.uuid4().hex + '.htm'
    file_path = dir_path + file_name
    with open(file_path, 'wb') as f:
        f.write(content)
    return file_path
