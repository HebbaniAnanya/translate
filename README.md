# Scalable AI Translation Engine: Architectural Evolution

This repository contains two distinct architectural iterations of a machine learning translation service. It serves as a case study in migrating a monolithic, blocking web application into a decoupled, distributed asynchronous pipeline designed for cloud scale.

---

## Architecture V2: Decoupled, Distributed System (Current Production Setup)
A high-performance, asynchronous microservice architecture built to isolate heavy machine learning workloads from the user-facing web tier.

### Key Features
* **Asynchronous Task Offloading:** Utilizes FastAPI to accept translation requests instantly, handing heavy computation over to an isolated background queue to maintain stable API responsiveness.
* **Decoupled Architecture:** Implements a **Redis** message broker to separate the API routing engine from the execution layer, ensuring traffic spikes never degrade the web tier.
* **Distributed Compute Workers:** Deploys a **Celery Worker** process pool optimized for handling sequential sequence-to-sequence ML translation tasks.
* **Local ML Model Inference:** Integrates Facebook's **NLLB-200** machine learning model directly inside the container runtime environment.
* **Enterprise Security & Observability:** Implements secure **JWT token authentication** alongside custom **ASGI logging middleware** for performance monitoring and execution tracking.

### Tech Stack
* **Framework:** FastAPI (Python 3.12)
* **Task Management:** Celery, Redis
* **AI/ML Integration:** Hugging Face Transformers (NLLB-200)
* **Infrastructure:** Docker, Docker Compose, AWS EC2

---

## Architecture V1: Monolithic In-Memory Service (Legacy Blueprint)
The initial prototype built to validate the core machine learning pipeline using local framework utilities.

### Key Features
* **In-Memory Task Management:** Leveraged FastAPI's native `BackgroundTasks` utility to handle text processing requests locally within the same application process.
## Overview
A containerized FastAPI application that translates English text to French using HuggingFace t5 model. Deployed on AWS EC2 with Docker.

## Features
- REST API endpoints for text translation
- Input validation with Pydantic
- Case-insensitive language handling (`English` / `French`)
- Secure JWT Authentication for user login, token generation, and route protection
- Asynchronous Background Tasks via FastAPI to handle long-running translation processes   without blocking responses
- Containerized with Docker for portability
- Deployed on AWS EC2 with security group configuration

* **Architectural Bottlenecks Identified:** High concurrent user traffic risked blocking the single Python event loop due to heavy CPU-bound model inference, highlighting the need to decouple compute from routing (solved in V2).

### Tech Stack
* **Framework:** FastAPI, Uvicorn
* **Task Utility:** FastAPI BackgroundTasks
* **AI/ML Integration:** HuggingFace Transformers
* **Database:** SQLite

---

## Deployment & Local Installation (Architecture V2)

### Prerequisites
* Docker & Docker Compose
* AWS EC2 Environment (Minimum 4GB Swap Space configured for ML model weights)

To deploy the active distributed infrastructure, clone the repository and execute:

```bash
docker compose up -d --build