import time
from tools import di
import sys
sys.path.append("..")


class BenchMark:

    def __init__(self):
        self.di = di.Di()
        self.redis = self.di.getRedis()
        self.mongo = self.di.getMongoDb()
        self.es = self.di.getElasticsearch()
        self.time_limit = 10

    def run(self):
        self.di.cost("开始")
        self.last = time.time()
        self.current = time.time()

        loop = True
        n = 0
        while loop:
            if self.isFullSec():
                loop = False
            else:
                # self.redis.set("test_key",n)
                self.mongo["test"]["test_data"].insert_one({"n": n})
                n += 1
                self.current = time.time()

    def isFullSec(self):
        if (self.current - self.last > self.time_limit):
            self.last = time.time()
            return True
        else:
            return False


m = BenchMark()
m.run()
