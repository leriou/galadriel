from pykafka import KafkaClient




class KafkaManager:

    def __init__(self):
        self.kafka = KafkaClient(hosts="127.0.0.1:9092")
        self.producer = None
        self.consumer = None

    def setTopic(self,topicName):
        print(self.kafka.topics)
        self.topic = self.kafka.topics[bytes(topicName,encoding="utf-8")]
        return self.topic

    def getTopics(self):
        return self.kafka.topics
    
    def getProducer(self):
        return self.topic.get_sync_producer()
    
    def getConsumer(self):
        return self.topic.get_simple_consumer()

    def test(self):
        self.setTopic('test1_topic')
        p = self.getProducer()
        for i in range(101,10000):
            p.produce(bytes("this is msg:" + str(i),encoding="utf8"))
        p.stop()

        c = self.getConsumer()
        for i in c:
            print("offset %s, value %s",(i.offset,i.value))    

if __name__ == "__main__":
    m = KafkaManager()
    m.test()
