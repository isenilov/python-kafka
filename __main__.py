import datetime
import os
from uuid import uuid4

from confluent_kafka import DeserializingConsumer, SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import StringDeserializer, StringSerializer

from helpers import todict
from protocol.Message import Message

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC_NAME = os.getenv("TOPIC_NAME")

schema_registry_client = SchemaRegistryClient({"url": "http://schemaregistry:8085"})

# --- Producing part ---

producer_conf = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                 "key.serializer": StringSerializer("utf_8"),
                 "value.serializer": AvroSerializer(schema_str=Message.schema,
                                                    schema_registry_client=schema_registry_client,
                                                    to_dict=todict)}

producer = SerializingProducer(producer_conf)

print(f"Producing message to topic '{TOPIC_NAME}'")

# Serve on_delivery callbacks from previous calls to produce()
producer.poll(0.0)

msg = Message(dict(
    timestamp=int(datetime.datetime.now().timestamp()),
    data=dict(
        count=10,
        value=100.0)))
producer.produce(topic=TOPIC_NAME,
                 key=str(uuid4()),
                 value=msg)
print(f"Produced message: {msg.dict()}")

print("\nFlushing records...")
producer.flush()

# --- Consuming part ---

consumer_conf = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                 "key.deserializer": StringDeserializer("utf_8"),
                 "value.deserializer": AvroDeserializer(schema_str=Message.schema,
                                                        schema_registry_client=schema_registry_client,
                                                        from_dict=lambda obj, _: Message(obj)),
                 "group.id": "test_group",
                 "auto.offset.reset": "earliest"}

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe([TOPIC_NAME])

while True:
    try:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        message = msg.value()
        if message is not None:
            print(f"Consumed message {message.dict()}")
    except KeyboardInterrupt:
        break

consumer.close()
