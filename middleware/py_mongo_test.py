from pymongo import MongoClient

class MongodbManager():

    def __init__(self):
        self.cli = MongoClient("127.0.0.1",27017)
    

    def insert(self):
        self.cli["local"]["test"].insert({"id":1,"name":"小明","age":10})
    
    def test(self):
        self.insert()

if __name__ == "__main__":
    n =  MongodbManager()
    n.test()