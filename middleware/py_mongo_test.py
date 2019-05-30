#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pymongo import MongoClient
import time
import json

class MongodbManager():

    def __init__(self):
        self.cli = MongoClient("127.0.0.1",27017)
        self.data = []
        
    def insert(self,info):
        self.cli["test_data"]["test_py_mongo"].insert_many(info)

    def init_data(self):
        for i in range(0,1000):
            info = {
                "id":i,
                "age":100,
                "local":True,
                "time":time.time()
            }
            self.data.append(info)
    
    def test(self):
        self.init_data()
        self.insert(self.data)

    def bak(self):
        result =  self.cli["admin"]["private"].find()
        ret = {}
        file = "pwd.config"
        for i in result.rewind():
            i.pop("_id")
            ret[i["appname"]] = i
        with open(file, "w+") as f:
            # for n in json.dumps(ret, ensure_ascii=False):
            #     print(n)
            for n in ret:
                f.write(n + "\n")
                ret[n].pop("appname")
                f.write(json.dumps(ret[n], ensure_ascii=False).strip("{}") + "\n\n")
        
        
if __name__ == "__main__":
    n =  MongodbManager()
    # n.test()
    n.bak()