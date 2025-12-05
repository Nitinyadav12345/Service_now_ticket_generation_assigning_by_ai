"""
Celery application configuration
"""
from celery import Celery
from celery.schedules import crontab
import os

# Get Redis URL from environment
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

# Create Celery app
celery_app = Celery(
    "jira_ai",
    broker=REDIS_URL,
    backend=os.getenv("CELERY_RESULT_BACKEND", REDIS_URL),
    include=[
        "app.tasks.capacity_tasks",
        "app.tasks.assignment_tasks",
        "app.tasks.learning_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Celery Beat schedule
celery_app.conf.beat_schedule = {
    # Sync capacity every 15 minutes
    "sync-capacity-every-15-min": {
        "task": "app.tasks.capacity_tasks.sync_capacity",
        "schedule": crontab(minute="*/15"),
    },
    # Process assignment queue every hour
    "process-assignment-queue-hourly": {
        "task": "app.tasks.assignment_tasks.process_assignment_queue",
        "schedule": crontab(minute=0),  # Every hour at minute 0
    },
    # Update learning models daily at 2 AM
    "update-learning-models-daily": {
        "task": "app.tasks.learning_tasks.update_learning_models",
        "schedule": crontab(hour=2, minute=0),
    },
}

if __name__ == "__main__":
    celery_app.start()
