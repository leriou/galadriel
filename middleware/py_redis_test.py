import redis
from rediscluster import StrictRedisCluster

class RedisManager:
    
    def __init__(self):
        self.cli = redis.Redis("127.0.0.1",6379)
        self.nodes = [
            {"host":"127.0.0.1","port":"7000"},
            {"host":"127.0.0.1","port":"7001"},
            {"host":"127.0.0.1","port":"7002"},
            {"host":"127.0.0.1","port":"7003"},
            {"host":"127.0.0.1","port":"7004"},
            {"host":"127.0.0.1","port":"7005"}
        ]
        # self.cluster = StrictRedisCluster(startup_nodes=self.nodes,decode_responses=True)

    def getRedis(self):
        return self.cli
    
    def get_cluster(self):
        return self.cluster
    
    def test(self):
        print("start")
        for i in range(0,1000):
            self.getRedis().set("as"+str(i*4),1001+i)
        print(self.getRedis().get("as0"))
        print("done")


if __name__ == "__main__":
    rm = RedisManager()
    rm.test()