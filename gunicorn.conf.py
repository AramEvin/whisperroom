# gunicorn.conf.py — Python config file for Gunicorn

bind             = "0.0.0.0:5000"
worker_class     = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
workers          = 1
threads          = 1
timeout          = 120
keepalive        = 5
graceful_timeout = 30
accesslog        = "-"
errorlog         = "-"
loglevel         = "info"
proc_name        = "whisperroom"
worker_connections = 1000
