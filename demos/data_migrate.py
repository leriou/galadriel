import sys 
sys.path.append("..") 
from tools import di

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
                "index":{
                    "_index":self.index,
                    "_type":self.type
                    }
            })     
            # c["id"] = c["_id"]           
            c.pop("_id")
            migrate.append(c)
        self.es.bulk(migrate)
                
    def get_source_data(self):
        self.data = []
        result = self.mongo[self.source_db][self.source_collection].find({})
        for n in result:
            self.data.append(n)  
        return self      

    def execute(self):
        self.get_source_data()._migrate()

m = Migrate()
# m.source("fzdm","mh_list")
# m.target("fzdm-mh-list","list")
# m.execute()
# m.source("fzdm","mh_pic")
# m.target("fzdm-mh-pic","pic")
# m.execute()
# m.source("fzdm","mh_subs")
# m.target("fzdm-mh-subs","subs")
# m.execute()

m.source("bitmap","user").target("bitmap","user").execute()
