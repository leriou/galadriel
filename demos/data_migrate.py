from tools import di
import sys
sys.path.append("..")


class Migrate():

    def __init__(self):
        self.di = di.Di()
        self.mongo = self.di.getMongoDb()
        self.es = self.di.getElasticsearch()
        self.index = None
        self.type = None

    def source(self, db, collection):
        self.source_db = db
        self.source_collection = collection
        return self

    def target(self, index, doc_type):
        self.index = index
        self.type = doc_type
        return self

    def _migrate(self):
        migrate = []
        for c in self.data:
            migrate.append({
                "index": {
                    "_index": self.index,
                    "_type": self.type,
                    "_id": c["_id"].__str__()
                },
                "timeout": 1000000
            })
            c.pop("_id")
            migrate.append(c)

        self.es.bulk(migrate)

    def get_source_data(self, limit=3000):
        self.data = []
        result = self.mongo[self.source_db][self.source_collection].find({})
        for n in result:
            self.data.append(n)
        return self

    def execute(self):
        self.get_source_data()._migrate()


m = Migrate()
m.source("zgzcw", "data").target("zgzcw", "_doc").execute()
m.source("mh", "mh-pics").target("mh-pics", "_doc").execute()
m.source("mh", "mh-list").target("mh-lists", "_doc").execute()
m.source("mh", "mh-subs").target("mh-subs", "_doc").execute()
