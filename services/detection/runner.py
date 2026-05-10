import json
from kafka import KafkaConsumer

from shared.config.settings import (
    WIFI_LOG_TOPIC,
    KAFKA_BOOTSTRAP_SERVERS
)

from services.detection.engine.processor import (
    process_event
)


consumer = KafkaConsumer(
    WIFI_LOG_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    group_id="detection-engine",
    value_deserializer=lambda m:
    json.loads(m.decode("utf-8"))
)


print("Detection engine running...")


for message in consumer:

    event = message.value

    alerts = process_event(event)

    if alerts:
        print("\n🚨 ALERT DETECTED")
        print(alerts)

