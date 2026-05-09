from dataclasses import dataclass
from typing import Literal
import time


EventType = Literal["AUTH_ATTEMPT", "ASSOCIATION", "DISASSOCIATION"]


@dataclass
class LogEvent:
    timestamp: int
    ap_id: str
    client_mac: str
    event_type: EventType
    status: str
    signal_strength: int
    ssid: str
    band: str
    channel: int

    @staticmethod
    def now():
        return int(time.time())

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "ap_id": self.ap_id,
            "client_mac": self.client_mac,
            "event_type": self.event_type,
            "status": self.status,
            "signal_strength": self.signal_strength,
            "ssid": self.ssid,
            "band": self.band,
            "channel": self.channel
        }



