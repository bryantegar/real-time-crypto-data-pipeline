# Real-Time Crypto Data Engineering Platform

## Overview

This project is a production-style real-time data pipeline that ingests cryptocurrency price streams and processes them using distributed streaming architecture.

It simulates a real-world fintech data engineering system demonstrating scalable ingestion, streaming computation, persistent storage, and live visualization.

---

## Architecture

Pipeline Flow:

```
Binance WebSocket → Kafka → Processing → Storage → Dashboard
```

---

## Features

* Real-time crypto price ingestion (BTCUSDT stream)
* Distributed streaming pipeline using Kafka
* Structured storage into PostgreSQL
* Live dashboard updates every 3 seconds
* Modular architecture design
* Containerized deployment with Docker

---

## Tech Stack

| Layer         | Technology             |
| ------------- | ---------------------- |
| Data Source   | Binance WebSocket API  |
| Streaming     | Apache Kafka           |
| Processing    | Python Streaming Logic |
| Storage       | PostgreSQL             |
| Visualization | Streamlit              |
| Deployment    | Docker Compose         |
| Language      | Python                 |

---

## Project Structure

```
src/
 ┣ collectors
 ┣ processing
 ┣ storage
 ┣ dashboard
 ┗ utils
```

---

## How to Run

Start services

```
docker compose up -d
```

Activate environment

```
venv\Scripts\activate
```

Run producer

```
python src\producer_crypto.py
```

Run consumer

```
python src\consumer_db.py
```

Run dashboard

```
streamlit run src\dashboard_realtime.py
```

---

## Engineering Concepts Demonstrated

* Real-time stream processing
* Event-driven architecture
* Distributed messaging systems
* Data pipeline orchestration
* Containerized deployment
* Scalable system design

---

## Use Case

This system simulates how financial platforms monitor live market data streams for analytics, alerting, and trading insights.

---

## Author

**Bryan Tegar**
Aspiring Data Engineer
