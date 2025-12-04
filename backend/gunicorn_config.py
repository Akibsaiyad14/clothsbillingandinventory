import multiprocessing

# Gunicorn configuration for Render
# Use minimal workers to save memory on free tier

workers = 1  # Use only 1 worker to minimize memory usage
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # Increase timeout to 5 minutes to prevent worker timeouts
keepalive = 5
graceful_timeout = 30

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'clothshop'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Memory management
max_requests = 1000
max_requests_jitter = 100

# Prevent memory leaks
preload_app = False
