from services.detection.rules.auth_spike import AuthSpikeRule
from services.detection.rules.rogue_mac import RogueMACRule
from services.detection.rules.signal_anomaly import SignalAnomalyRule

rules = [
    AuthSpikeRule(),
    RogueMACRule(),
    SignalAnomalyRule()
]


def process_event(event: dict):

    alerts = []

    for rule in rules:
        result = rule.evaluate(event)

        if result:
            alerts.append(result)

    return alerts

