# 🛡️ FinGuard: Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)

**FinGuard** is a scalable, event-driven microservices architecture designed to detect financial fraud in real-time. It processes high-volume transaction streams, identifies suspicious patterns (e.g., impossible travel, high-value transactions) using stateful analysis, and provides real-time observability.

## Architecture

The system follows a modern **Big Data Pipeline** architecture:

```mermaid
graph LR
    A[Transaction Simulator] -->|JSON Stream| B(Apache Kafka)
    B -->|Consumer| C{Fraud Detector}
    C <-->|State Cache| D[(Redis)]
    C -->|Persist Fraud| E[(PostgreSQL)]
    E -->|Query| G[FastAPI Backend]
    G -->|Visualize| H[Streamlit Dashboard]

Key Features
Real-Time Stream Processing: Ingests transaction data via Apache Kafka.

Stateful Pattern Detection: Uses Redis to track user locations and detect "Impossible Travel" anomalies (e.g., a user appearing in New York 1 minute after a transaction in Istanbul).

Fault Tolerance: Implements Dead Letter Queues (DLQ) to handle poisonous messages gracefully.

Security: Secured API endpoints using JWT (JSON Web Token) authentication.

Interactive Dashboard: A real-time Streamlit dashboard to monitor alerts and statistics.

Tech Stack
Language: Python 3.9+

Message Broker: Apache Kafka

Databases: PostgreSQL (Persistent Storage), Redis (In-Memory Cache)

Backend API: FastAPI, Pydantic, JWT

Frontend: Streamlit

Installation & Setup
Prerequisites
Ensure you have the following services running locally on their default ports:

Apache Kafka (Port 9092) & Zookeeper

Redis (Port 6379)

PostgreSQL (Port 5432) - Database named finguard

1. Clone the Repository
Bash

git clone [https://github.com/yourusername/finguard.git](https://github.com/yourusername/finguard.git)
cd finguard
2. Install Dependencies
It is recommended to use a virtual environment.

Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Database Configuration
Ensure your PostgreSQL database is running. The application will automatically create the necessary tables on the first run.

Default credentials configured in code: user: admin, password: password123. (You can change these in api.py and detector.py).

Usage (Running the Modules)
You need to run each service in a separate terminal window.

Terminal 1: The Transaction Generator (Producer) Starts generating synthetic transaction data.

Bash

python producer.py
Terminal 2: The Fraud Detector (Consumer) Listens to Kafka, analyzes transactions, and logs frauds to DB.

Bash

python detector.py
Terminal 3: The Backend API Starts the FastAPI server (Access at http://localhost:8000/docs).

Bash

uvicorn api:app --reload
Terminal 4: The Dashboard Starts the visualization interface.

Bash

streamlit run dashboard.py
Project Structure
Bash

finguard/
├── api.py           # FastAPI Backend & JWT Auth
├── dashboard.py     # Streamlit Real-time Dashboard
├── detector.py      # Stream Processing Logic (Kafka Consumer)
├── producer.py      # Synthetic Data Generator (Kafka Producer)
├── requirements.txt # Python dependencies
└── README.md        # Project Documentation
🔮 Future Roadmap
[ ] Containerization with Docker & Kubernetes.

[ ] Integration with Spark Streaming for windowed aggregations.

[ ] Machine Learning model integration for advanced anomaly detection.


