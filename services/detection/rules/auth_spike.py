from services.detection.rules.base_rule import BaseRule
from services.detection.state.redis_client import redis_client


class AuthSpikeRule(BaseRule):

    WINDOW_SECONDS = 60
    THRESHOLD = 10

    def evaluate(self, event: dict):

        if event["status"] != "FAIL":
            return None

        mac = event["client_mac"]

        key = f"auth_fail:{mac}"

        count = redis_client.incr(key)

        if count == 1:
            redis_client.expire(
                key,
                self.WINDOW_SECONDS
            )

        if count >= self.THRESHOLD:
            return {
                "type": "AUTH_SPIKE",
                "severity": "HIGH",
                "mac": mac,
                "count": count
            }

        return None
