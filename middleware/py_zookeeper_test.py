from kazoo.client import KazooClient

class ZkClient:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "2181"
    
    def getClient(self):
        return KazooClient(hosts=self.host+":"+self.port)

zk = ZkClient().getClient()

zk.start()

node = "/test-zk-py"
node_sub2 = "/test-zk-py/test2"
if not zk.exists(node):
    zk.create_async(node)

zk.create_async(node_sub2,b'this is a test',None,False)

print(zk.get_children("/"))


