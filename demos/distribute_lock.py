
from tools import di
import sys
sys.path.append("..")


class DistributeLock:

    def __init__(self):
        self.redis = di.Di().getRedis()

    def lock(self, key):
        if self.redis.setnx(key, 1):
            self.redis.expire(key, 300)
            return True
        else:
            return False

    def unlock(self, key):
        self.redis.expire(key, -1)
        return True


lock = DistributeLock()

resource = "distribute1"
res = lock.lock(resource)
if res:
    print("获取锁成功")
else:
    print("获取锁失败")

res = lock.unlock(resource)
