import multiprocessing
import os

# Bind to all interfaces on port from env or default 8000
bind = os.getenv("BIND", "0.0.0.0:8000")
# Use uvicorn workers for ASGI
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"
# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
# Graceful timeouts
timeout = int(os.getenv("TIMEOUT", 30))
