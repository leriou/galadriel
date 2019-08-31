import redis


class RedisManager:
    
    def __init__(self):
        self.cli = redis.Redis("127.0.0.1",6379)

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