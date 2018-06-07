
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import redis
import pymysql as mysql
import elasticsearch
import config

'''
依赖注入
'''


class Di:

    def __init__(self):
        Di.config = config.ConfigParser().getContent("config.ini")
        Di.redis = None
        Di.mongodb = None
        Di.es = None

    # redis client
    def getRedis(self):
        if Di.redis == None:
            Di.redis = redis.Redis(Di.config.get("redis", "host"),
                                   int(Di.config.get("redis", "port")))
        return Di.redis

    # mongodb client
    def getMongoDb(self):
        if Di.mongodb == None:
            Di.mongodb = MongoClient(Di.config.get("mongodb", "host"),
                                     int(Di.config.get("mongodb", "port")))
        return Di.mongodb

    # mysql client
    def getMysql(self):
        if Di.mysql == None:
            Di.mysql = mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='password')
        return Di.mysql.cursor()

    def getElasticsearch(self):
        if Di.es == None:
            Di.es = elasticsearch.Elasticsearch(["localhost:9200"])
        return Di.es

    def test(self, flag):
        if flag == 'es':
            cli = self.getElasticsearch()
            cli.index(index="test",doc_type="match",body={"name":"test","age":10})
            data = cli.search(index="test", doc_type="match",body={"query":{"match_all":{}},"size":2} )
        if flag == 'mongodb':
            cli = self.getMongoDb()
            db = cli.test.test
            db.insert({"test": "success"})
            data = db.find_one()
        if flag == 'redis':
            cli = self.getRedis()
            cli.set("test_file", "redis test success")
            data = cli.get("test_file")

        if flag == 'mysql':
            cli = self.getMysql()
            data = 'success'
        print(data)


if __name__ == '__main__':
    m = Di()
    m.test('es')
