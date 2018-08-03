import redis


class RedisManager:
    
    def __init__(self):
        self.cli = redis.Redis("127.0.0.1",6379)

    def getRedis(self):
        return self.cli
    
    def test(self):
        self.cli.set("testa","aaa")
        print(self.cli.get("testa"))


if __name__ == "__main__":
    r = RedisManager()
    r.test()