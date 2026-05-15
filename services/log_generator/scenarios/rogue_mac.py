import random

from shared.models.log_event import (
    LogEvent
)
from shared.constants.events_info import BAND, CHANNELS_5GHz, CHANNELS_2_4GHz


def rogue_mac_event():
    rogue_macs = [
        "FA:KE:11:22:33:44",
        "EV:IL:55:66:77:88"
    ]

    band = random.choice(BAND)

    return LogEvent(
        timestamp=LogEvent.now(),
        ap_id=random.choice([
            "ap-1",
            "ap-2",
            "ap-5"
        ]),
        client_mac=random.choice(
            rogue_macs
        ),
        event_type="AUTH_ATTEMPT",
        status="SUCCESS",
        signal_strength=random.randint(
            -60,
            -40
        ),
        ssid="OfficeWiFi",
        band=band,
        channel=random.choice(CHANNELS_2_4GHz) if band == '2.4' else random.choice(CHANNELS_5GHz)
    )
