import random

from shared.models.log_event import (
    LogEvent
)
from shared.constants.events_info import BAND, CHANNELS_5GHz, CHANNELS_2_4GHz


def signal_anomaly_event():
    band = random.choice(BAND)
    return LogEvent(
        timestamp=LogEvent.now(),
        ap_id="ap-1",
        client_mac="AA:BB:CC:DD:EE:01",
        event_type="AUTH_ATTEMPT",
        status="SUCCESS",

        # intentionally suspicious
        signal_strength=random.choice([
            -90,
            -25
        ]),
        band=band,
        channel=random.choice(CHANNELS_2_4GHz) if band == '2.4' else random.choice(CHANNELS_5GHz),
        ssid="OfficeWiFi"
    )

