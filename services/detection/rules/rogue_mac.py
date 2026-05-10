from services.detection.rules.base_rule import (
    BaseRule
)

from shared.config.known_devices import (
    KNOWN_MACS
)


class RogueMACRule(BaseRule):

    def evaluate(self, event: dict):

        mac = event["client_mac"]

        if mac not in KNOWN_MACS:

            return {
                "type": "ROGUE_MAC",
                "severity": "MEDIUM",
                "mac": mac,
                "ap_id": event["ap_id"]
            }

        return None

