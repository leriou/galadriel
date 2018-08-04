import elasticsearch


class ElasticsearchManager:

    def __init__(self):
        self.cli = elasticsearch.Elasticsearch(["localhost:9200"])
    
    def add(self):
        self.cli.index(index="test_py",doc_type="match",body={"name":"test","age":10,"type":"test"})
    
    def search(self):
        print(self.cli.search(index="test_py", doc_type="match",body={"query":{"match_all":{}},"size":20} ))

    def test(self):
        self.add()
        self.search()

if __name__ == "__main__":
    e = ElasticsearchManager()
    e.test()