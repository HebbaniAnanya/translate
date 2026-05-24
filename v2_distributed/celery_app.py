import os
from celery import Celery
from playhouse.pwasyncio import AsyncSqliteDatabase

# message broker location (Redis)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery
celery_app = Celery(
    "translation_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Celery configuration tweaks
celery_app.conf.update(
    task_track_started=True,
    timezone='UTC'
)

import tasks