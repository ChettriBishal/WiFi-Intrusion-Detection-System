import random
import time
from shared.models.log_event import LogEvent
from shared.constants.events_info import APS, SSIDS, MACS, BAND, CHANNELS_5GHz, CHANNELS_2_4GHz
from services.log_generator.scenarios.auth_attack import auth_attack
from services.log_generator.scenarios.rogue_mac import rogue_mac_event
from .producer import send_event
from shared.config.settings import WIFI_LOG_TOPIC


def generate_normal_event():
    band = random.choice(BAND)
    return LogEvent(
        timestamp=LogEvent.now(),
        ap_id=random.choice(APS),
        client_mac=random.choice(MACS),
        event_type="AUTH_ATTEMPT",
        status=random.choice(["SUCCESS", "FAIL"]),
        signal_strength=random.randint(-80, -40),
        ssid=random.choice(SSIDS),
        band=band,
        channel=random.choice(CHANNELS_2_4GHz) if band == '2.4' else random.choice(CHANNELS_5GHz)
    )


def run():
    while True:
        # 65% normal traffic, 15% rogue, 20% auth attack
        choice = random.random()
        if choice < 0.65:
            event = generate_normal_event()
            send_event(
                WIFI_LOG_TOPIC,
                event.to_dict()
            )
            print(f"Sent: {event}")
        elif choice < 0.80:  # rogue ap
            event = rogue_mac_event()
            send_event(
                WIFI_LOG_TOPIC,
                event.to_dict()
            )
            print(f"Sent rogue event: {event}")
        else:
            events = auth_attack()
            for event in events:
                send_event(
                    WIFI_LOG_TOPIC,
                    event.to_dict()
                )
                print(f"Sent attack event: {event}")

        time.sleep(1)


if __name__ == "__main__":
    run()
