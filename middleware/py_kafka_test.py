from pykafka import KafkaClient,Cluster

class KafkaManager:

    def __init__(self):
        self.hosts = "127.0.0.1:9092"
        self.kafka = KafkaClient(self.hosts)
        self.producer = None
        self.consumer = None

    def str_to_bytes(self, sstring):
        return bytes(string, encoding="utf-8")

    def setTopic(self,topic_name):
        self.topic = self.kafka.topics[self.str_to_bytes(topic_name)]
        return self.topic

    def getTopics(self):
        return self.kafka.topics

    def updateTopic(self, meta):
        self.topic.update(meta)

    def getLatestAvailableOffsets(self):
        return self.topic.latest_available_offsets()

    def getProducer(self):
        return self.topic.get_sync_producer()
    
    def getConsumer(self, consumer_group):
        return self.topic.get_balanced_consumer(self.str_to_bytes(consumer_group),True)

    def test(self):
        self.setTopic('py-topic')
        p = self.getProducer()
        for i in range(101,10000):
            p.produce(self.str_to_bytes("this is msg:" + str(i)))
        p.stop()

        c = self.getConsumer("consumer-py3")
        for i in c:
            print("offset: "+str(i.offset)+" value: "+str(i.value))    

if __name__ == "__main__":
    m = KafkaManager()
    m.test()
