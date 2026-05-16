"""
Celery Application Initialization
"""

from celery import Celery

celery_app = Celery(
    "ai_pdf_reader",
    include=[
        "app.tasks.document_tasks",
        "app.tasks.chat_tasks",
    ],
)

celery_app.config_from_object("app.worker.celery_config")