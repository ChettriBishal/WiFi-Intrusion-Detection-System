from services.detection.rules.base_rule import (
    BaseRule
)

from services.detection.state.redis_client import (
    redis_client
)


class SignalAnomalyRule(BaseRule):
    THRESHOLD = 20

    def evaluate(self, event: dict):

        mac = event["client_mac"]
        ap_id = event["ap_id"]

        signal = event[
            "signal_strength"
        ]

        key = (
            f"signal_baseline:"
            f"{mac}:{ap_id}"
        )

        previous = redis_client.get(
            key
        )

        # first observation
        if previous is None:
            redis_client.set(
                key,
                signal
            )
            return None

        previous = int(previous)

        delta = abs(
            signal - previous
        )

        # update baseline
        smoothed_signal = int(
            (previous * 0.8) +
            (signal * 0.2)
        )

        redis_client.set(
            key,
            smoothed_signal
        )

        if delta >= self.THRESHOLD:
            return {
                "type": "SIGNAL_ANOMALY",

                "severity": "MEDIUM",

                "mac": mac,

                "ap_id": ap_id,

                "baseline": previous,

                "current": signal,

                "delta": delta
            }

        return None
