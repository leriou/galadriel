import elasticsearch
import time
import uuid

class ElasticsearchManager:

    def __init__(self):
        self.cli = elasticsearch.Elasticsearch(["localhost:9200"])
    
    def add(self):
        # self.cli.index(index="test_py",doc_type="match",body={"name":"test","age":10,"type":"test","subs":[1,2,3,4],"update_time":time.time()})
        self.cli.index(index="test_py",doc_type="match",body={"name":"test","age":10,"type":"test","subs":[1,2,3,4],"update_time":time.time()})

    def search(self):
        print(self.cli.search(index="test_py", doc_type="match",body={"query":{"match_all":{}},"size":20} ))

    def test(self):
        self.add()
        for i in range(0,1000):
            info = {
                "id":uuid.uuid1(),
                "time":time.time(),
                "name": str(i) +"ming",
                "age": 9
            }
            self.cli.create(index="test-py-2",doc_type="test-infos",body=info,id=info["id"])
            self.cli.index(index="test-py-1",doc_type="test-infos",body=info)
        self.search()
    
    def delete(self):
        self.cli.delete_by_query(index="score_test",doc_type="text",query={"query":{"match":{"content":"测试"}}})

if __name__ == "__main__":
    e = ElasticsearchManager()
    e.test()