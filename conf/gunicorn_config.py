command = '~/Edulethics-Development/venv/bin/gunicorn'
pythonpath = '~/Edulethics-Development/venv/bin/python'
bind = '0.0.0.0:443'
workers = 12
certfile = '/etc/letsencrypt/live/backend.eduethics.com/fullchain.pem'
keyfile = '/etc/letsencrypt/live/backend.eduethics.com/privkey.pem'
ca_certs = '/etc/letsencrypt/live/backend.edulethics.com/cert.pem'
accesslog = 'access_log'
errorlog = 'error_log'
loglevel = 'debug'
syslog = True
syslog_prefix = 'EDULETHICS'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
worker_class = 'gevent'
timeout = 0
do_handshake_on_connect=False
limit_request_line = 0

