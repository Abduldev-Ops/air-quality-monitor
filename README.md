# Air Quality Monitor

A full-stack IoT system that reads environmental data from an ESP32 sensor node,
publishes over MQTT, stores in a time-series database, and visualizes on a
React dashboard with SMS alerts.

---

## What it does

- ESP32 reads temperature, humidity, and pressure from **BMP280** over I2C
- Publishes JSON payloads to **HiveMQ Cloud** MQTT broker every 10 seconds
- Python **Flask** backend subscribes to MQTT and writes to **InfluxDB Cloud**
- **React** frontend displays live readings and historical trend charts
- SMS alert via **Twilio** when readings cross configured thresholds

---

## Architecture

```
ESP32 + BMP280
      │
      │ MQTT (JSON payload)
      ▼
HiveMQ Cloud Broker
      │
      │ paho-mqtt subscribe
      ▼
Flask Backend ──────► InfluxDB Cloud
                              │
                              │ HTTP query
                              ▼
                       React Dashboard
                       (live + historical)
```

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Firmware | C++ (ESP32 Arduino) |
| Protocol | MQTT (HiveMQ Cloud) |
| Backend | Python · Flask · paho-mqtt |
| Database | InfluxDB Cloud (time-series) |
| Frontend | React · Chart.js |
| Alerts | Twilio SMS API |

---

## Design decisions

**Why MQTT over HTTP polling?**
HTTP polling at 10s intervals means the backend repeatedly opens connections
and waits even when no data has changed. MQTT is event-driven — the broker
pushes data to the backend the moment it arrives, with persistent connection
overhead amortized across all messages. For a sensor publishing continuously,
MQTT reduces both latency and connection overhead.

**Why InfluxDB over SQLite or PostgreSQL?**
Sensor readings are append-only time-series data — they're never updated,
rarely deleted, and queried almost exclusively by time range. InfluxDB's
data model is optimized exactly for this: automatic timestamping, efficient
range queries, built-in downsampling, and Flux query language for
time-series aggregations. A relational database would require manual
timestamp indexing and lacks native downsampling.

**Why HiveMQ Cloud over a self-hosted broker?**
Self-hosting a Mosquitto broker adds infrastructure management overhead with
no benefit for a single-node sensor system. HiveMQ Cloud provides a free
tier with TLS-secured connections and 99.9% uptime SLA — the right tradeoff
for a development and portfolio project.

---

## Running locally

**Requirements:** Python 3.10+, Node.js 18+, HiveMQ Cloud account,
InfluxDB Cloud account, Twilio account

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env      # fill in MQTT, InfluxDB, Twilio credentials
python app.py

# Frontend
cd frontend
npm install
npm start
```

**ESP32 firmware:**
Open `firmware/air_quality.ino` in Arduino IDE, fill in WiFi and MQTT
credentials, flash to ESP32.

---

## Hardware

| Component | Interface |
|-----------|-----------|
| ESP32 DevKit | — |
| BMP280 | I2C |

---

## Repository structure

```
firmware/          — ESP32 Arduino sketch
backend/
  app.py           — Flask app + MQTT subscriber + InfluxDB writer
  requirements.txt
frontend/
  src/
    App.jsx        — Main dashboard component
    components/    — Chart components
```