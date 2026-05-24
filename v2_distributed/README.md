# FastAPI Translation Service

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

## Requirements
- Docker
- Python 3.9+
- FastAPI, Uvicorn
- HuggingFace Transformers

## Usage
Build and run locally:
```bash
docker build -t fastapi-translate .
docker run -p 8000:8000 fastapi-translate
