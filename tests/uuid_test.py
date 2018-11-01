import uuid
import sys 
sys.path.append("..") 
import time
from pymongo import MongoClient
from tools.di import *


mongo = Di().getMongoDb()

obj_list = []
for i in range(0,10000):
    
    obj = {
        "uuid":str(uuid.uuid1()),
        "time":time.time()
    }
    obj_list.append(obj)
    

mongo["test"]["test_uuid"].insert_many(obj_list)

