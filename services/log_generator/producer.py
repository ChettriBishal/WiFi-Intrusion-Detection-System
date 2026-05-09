import json
from kafka import KafkaProducer

from shared.config.settings import (
    KAFKA_BOOTSTRAP_SERVERS
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    # key_serializer=str.encode,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)


def send_event(topic: str, event: dict):
    print(f"Inside send event producer from topic {topic}\n {event}")
    producer.send(topic, event)
    producer.flush()

