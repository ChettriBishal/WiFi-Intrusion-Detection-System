# WiFi Intrusion Detection System (WIDS)

A real-time **WiFi Intrusion Detection System (WIDS)** built using an event-driven architecture to simulate, ingest, process, and detect suspicious WiFi activity.

This project focuses on **backend engineering + WiFi/security domain knowledge**, combining:

* Real-time event streaming
* Stateful anomaly detection
* Redis-backed signal analysis
* Rule-based detection engine (mini SIEM-style architecture)

---

## Why This Project?

Most anomaly detection projects stop at log parsing.

This system is designed to resemble a **production-inspired WiFi intrusion detection pipeline**, leveraging:

* WiFi telemetry
* Event streaming
* Stateful processing
* Security-oriented detection logic

---

# Features Implemented

### Event Simulation

Simulates realistic WiFi telemetry:

* Authentication attempts
* Success/failure events
* RSSI (signal strength)
* AP activity
* Client MAC activity

### Attack Simulations

#### Authentication Spike Attack

Simulates repeated failed authentication attempts.

Example:

```text
AA:BB:CC:DD:EE:01
FAIL x20 in short duration
```

#### Rogue MAC Detection

Detects unknown devices attempting to authenticate.

Example:

```text
FA:KE:11:22:33:44
```

#### Signal Anomaly Detection

Detects suspicious RSSI deviations using adaptive baselines.

Example:

```text
Expected: -50 dBm
Observed: -90 dBm
```

---

# System Architecture

<img width="778" height="771" alt="wifis" src="https://github.com/user-attachments/assets/152af9c7-295b-4ec4-8ef7-d819678f5981" />


---

# Tech Stack

| Layer                  | Technology              |
| ---------------------- | ----------------------- |
| Language               | Python                  |
| Event Streaming        | Kafka                   |
| Stateful Processing    | Redis                   |
| API Layer (Upcoming)   | FastAPI                 |
| Persistence (Upcoming) | DynamoDB                |
| Messaging              | Kafka Producer/Consumer |
| Containerization       | Docker                  |

---

# Project Structure

```text
wifi-ids/
│
├── services/
│   ├── log_generator/
│   │   ├── generator.py
│   │   ├── producer.py
│   │   └── scenarios/
│   │       ├── auth_attack.py
│   │       ├── rogue_mac.py
│   │       └── signal_anomaly.py
│   │
│   ├── ingestion/
│   │   └── consumer.py
│   │
│   └── detection/
│       ├── engine/
│       │   └── processor.py
│       │
│       ├── rules/
│       │   ├── base_rule.py
│       │   ├── auth_spike.py
│       │   ├── rogue_mac.py
│       │   └── signal_anomaly.py
│       │
│       ├── state/
│       │   └── redis_client.py
│       │
│       └── runner.py
│
├── infrastructure/
│   └── kafka/
│       └── docker-compose.yml
│
├── shared/
│   ├── config/
│   │   ├── settings.py
│   │   └── known_devices.py
│   │
│   └── models/
│       ├── log_event.py
│       └── alert.py
│
├── requirements.txt
└── README.md
```

---

# Setup

## 1. Clone Repository

```bash
git clone <repo-url>
cd wifi-ids
```

---

## 2. Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start Infrastructure

Start Kafka + Redis:

```bash
cd infrastructure/kafka
docker compose up -d
```

Verify containers:

```bash
docker ps
```

You should see:

* Kafka
* Zookeeper
* Redis

---

# Running the Project

Open **3 terminals**.

---

## Terminal 1 — Detection Engine

Starts Kafka consumer + rule evaluation pipeline.

From project root:

```bash
python -m services.detection.runner
```

Expected:

```text
Detection engine running...
```

---

## Terminal 2 — WiFi Event Generator

Starts WiFi telemetry simulation.

From project root:

```bash
python -m services.log_generator.generator
```

This continuously generates:

* Normal WiFi traffic
* Authentication spikes
* Rogue MAC events
* Signal anomalies

Expected:

```text
Sent: LogEvent(...)
```

---

## Terminal 3 — Kafka Consumer (Optional Debugging)

For observing raw Kafka events.

```bash
python -m services.ingestion.consumer
```

Expected:

```text
{
    'timestamp': 1714829200,
    'ap_id': 'ap-1',
    'client_mac': 'AA:BB:CC:DD:EE:01',
    'event_type': 'AUTH_ATTEMPT',
    'status': 'FAIL',
    'signal_strength': -66
}
```

---

# Detection Rules

## 1. Authentication Spike Detection

Detects repeated failed authentication attempts within a time window.

### Logic

* Redis counter per MAC
* Sliding 60-second window
* Alert triggered after threshold exceeded

Example:

```text
20 failed logins in < 60 seconds
```

Alert:

```json
{
  "type": "AUTH_SPIKE",
  "severity": "HIGH",
  "mac": "AA:BB:CC:DD:EE:01",
  "count": 20
}
```

---

## 2. Rogue MAC Detection

Detects devices outside trusted inventory.

### Logic

Checks:

```text
client_mac ∉ known_devices
```

Alert:

```json
{
  "type": "ROGUE_MAC",
  "severity": "MEDIUM",
  "mac": "FA:KE:11:22:33:44",
  "ap_id": "ap-2"
}
```

---

## 3. Signal Anomaly Detection

Detects suspicious RSSI changes.

### Logic

Uses:

* Adaptive signal baseline
* Exponential Moving Average (EMA)
* Redis-backed state

Formula:

```text
smoothed_signal =
(previous × 0.8) +
(current × 0.2)
```

This reduces false positives caused by natural WiFi signal fluctuations.

Alert:

```json
{
  "type": "SIGNAL_ANOMALY",
  "severity": "MEDIUM",
  "mac": "AA:BB:CC:DD:EE:01",
  "ap_id": "ap-1",
  "baseline": -51,
  "current": -90,
  "delta": 39
}
```

---

# Example Detection Flow

```text
WiFi Event Generated
        ↓
Kafka Topic
        ↓
Detection Engine
        ↓
Rule Dispatcher
        ├── AuthSpikeRule
        ├── RogueMACRule
        └── SignalAnomalyRule
                ↓
            Redis State
                ↓
             Alert Output
```

---

# Future Roadmap

### Planned Features

* FastAPI REST API
* WebSocket live alerts
* Alert persistence
* DynamoDB integration
* Configurable JSON rule engine (mini SIEM)
* Metrics & observability
* Dashboard
* Roaming anomaly detection
* AP spoofing detection



# License

MIT License
