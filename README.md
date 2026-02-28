# Real-time Crypto Streaming Platform

This project is a real-time data pipeline using:
- Binance WebSocket (crypto ticker stream)
- Apache Kafka for streaming pipeline
- PostgreSQL for persistent storage
- Streamlit Dashboard for live monitoring

## Architecture
WebSocket → Kafka → PostgreSQL → Dashboard

## Features
- Real-time BTCUSDT price ingestion
- Structured storage into database (id, symbol, price, timestamp)
- Live dashboard updates every 3 seconds
- Fully containerized using Docker

## Tech Stack
| Component | Technology |
|----------|------------|
| Data Source | Binance WebSocket API |
| Streaming | Kafka |
| Storage | PostgreSQL |
| Dashboard | Streamlit |
| Deployment | Docker Compose |
| Language | Python |

## Dashboard Preview
(Screenshot here)

## How to Run
```sh
# Start Docker services
docker compose up -d

# Activate virtual environment
venv\Scripts\activate

# Run Kafka producer
python src\producer_crypto.py

# Run Kafka → DB consumer
python src\consumer_db.py

# Run dashboard
streamlit run src\dashboard_realtime.py

