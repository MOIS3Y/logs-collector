import environ
import gunicorn

from logs_collector.settings import BASE_DIR

# █▀▀ █░█ █▄░█ █ █▀▀ █▀█ █▀█ █▄░█   █▀▀ █▀█ █▄░█ █▀▀ █ █▀▀ ▀
# █▄█ █▄█ █░▀█ █ █▄▄ █▄█ █▀▄ █░▀█   █▄▄ █▄█ █░▀█ █▀░ █ █▄█ ▄
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# https://docs.gunicorn.org/en/stable/settings.html
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

env = environ.Env(
    # set casting, default value:
    GUNICORN_SERVER_NAME=(str, 'undisclosed'),
    GUNICORN_BIND=(str, '0.0.0.0:8000'),
    GUNICORN_BACKLOG=(int, 2048),

    GUNICORN_WORKERS=(int, 2),
    GUNICORN_WORKER_CLASS=(str, 'sync'),
    GUNICORN_WORKER_CONNECTIONS=(int, 1000),
    GUNICORN_THREADS=(int, 2),
    GUNICORN_TIMEOUT=(int, 3600),
    GUNICORN_KEEPALIVE=(int, 2),

    GUNICORN_LOGLEVEL=(str, 'info'),
)

environ.Env.read_env(BASE_DIR / '.env')

# Server name:
gunicorn.SERVER = env('GUNICORN_SERVER_NAME')

# Server socket:
bind = env('GUNICORN_BIND')
backlog = env('GUNICORN_BACKLOG')

# Worker processes:
workers = env('GUNICORN_WORKERS')
worker_class = env('GUNICORN_WORKER_CLASS')
worker_connections = env('GUNICORN_WORKER_CONNECTIONS')
threads = env('GUNICORN_THREADS')
timeout = env('GUNICORN_TIMEOUT')
keepalive = env('GUNICORN_KEEPALIVE')

# Logging:
loglevel = env('GUNICORN_LOGLEVEL')
errorlog = '-'
accesslog = '-'
access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'  # noqa:E501
