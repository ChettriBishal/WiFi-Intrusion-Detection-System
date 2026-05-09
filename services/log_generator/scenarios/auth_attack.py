import random
from shared.models.log_event import LogEvent
from shared.constants.events_info import BAND, APS, MACS, CHANNELS_5GHz, CHANNELS_2_4GHz


def auth_attack():
    band = random.choice(BAND)
    return [
        LogEvent(
            timestamp=LogEvent.now(),
            ap_id=random.choice(APS),
            client_mac=random.choice(MACS),
            event_type="AUTH_ATTEMPT",
            status="FAIL",
            signal_strength=random.randint(-70, -50),
            ssid="OfficeWiFi",
            band=band,
            channel=random.choice(CHANNELS_2_4GHz) if band == '2.4' else random.choice(CHANNELS_5GHz)
        )
        for _ in range(20)
    ]
