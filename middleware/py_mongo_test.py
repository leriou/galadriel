from pymongo import MongoClient
import time

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
        
if __name__ == "__main__":
    n =  MongodbManager()
    n.test()