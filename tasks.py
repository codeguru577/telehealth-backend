import os
from celery import Celery
import random

CELERY_BROKER_URL = os.getenv("REDIS_SERVER", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_SERVER", "redis://localhost:6379/0")


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name='tasks', bind=True)
def send_notification(self, patient_contact):
    # Simulate 25% failure rate
    import time
    time.sleep(3)
    if random.random() < 0.25:
        return {"result": f"Sending notification failed!"}
    return {"result": f"Notification sent successfully to {patient_contact}"}