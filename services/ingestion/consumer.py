import json
from kafka import KafkaConsumer

from shared.config.settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    WIFI_LOG_TOPIC
)

consumer = KafkaConsumer(
    WIFI_LOG_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    group_id="wifi-ids-group",
    value_deserializer=lambda m: json.loads(
        m.decode("utf-8")
    )
)

print("Listening for events...\n")

for message in consumer:
    print(message.value)

