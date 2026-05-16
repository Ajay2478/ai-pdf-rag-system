"""
Celery Configuration (Production-Ready Base)
"""

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

# Serialization
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"

# Time settings
timezone = "Asia/Kolkata"
enable_utc = True

# Reliability
task_track_started = True
task_time_limit = 600  # hard timeout
task_soft_time_limit = 540

# Retry defaults
task_acks_late = True
worker_prefetch_multiplier = 1  # prevents task overload

# Logging
worker_hijack_root_logger = False