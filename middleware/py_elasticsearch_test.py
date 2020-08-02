import elasticsearch
import time
import uuid


class ElasticsearchManager:

    def __init__(self):
        self.cli = elasticsearch.Elasticsearch(["localhost:9200"])
        self.data = []
        self.index = "test_data"
        self.type = "_doc"

    def init_data(self):
        for i in range(0, 1000):
            info = {
                "id": uuid.uuid1(),
                "time": time.time(),
                "name": str(i) + "ming",
                "age": 9
            }
            self.data.append(info)

    def add(self):
        for rec in self.data:
            self.cli.index(index=self.index, doc_type=self.type, body=rec)

    def bulk(self):
        bulk = []
        for c in self.data:
            bulk.append({
                "index": {
                    "_index": self.index,
                    "_type": self.type
                }
            })
            bulk.append(c)
        self.cli.bulk(bulk)

    def search(self):
        print(self.cli.search(index=self.index, doc_type=self.type,
                              body={"query": {"match_all": {}}, "size": 20}))

    def test(self):
        self.init_data()
        self.bulk()
        self.search()


if __name__ == "__main__":
    e = ElasticsearchManager()
    e.test()
