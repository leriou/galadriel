from pymongo import MongoClient
import time

class MongodbManager():

    def __init__(self):
        self.cli = MongoClient("127.0.0.1",27017)
    
    def insert(self,info):
        self.cli["local"]["test_py_mongo"].insert(info)
    
    def test(self):
        for i in range(0,1000):
            info = {
                "id":i,
                "age":100,
                "local":True,
                "time":time.time()
            }
            self.insert(info)

if __name__ == "__main__":
    n =  MongodbManager()
    n.test()