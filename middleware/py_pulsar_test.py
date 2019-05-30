import pulsar 


import pulsar

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('my-topic')
consumer = client.subscribe('my-topic', subscription_name='my-sub')



for i in range(1000):
    producer.send(('hello-pulsar-%d' % i).encode('utf-8'))


while True:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)

client.close()