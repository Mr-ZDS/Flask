import multiprocessing
import os

current_path = os.getcwd()
file_name = 'gunicorn'

log_path = os.path.join(current_path, 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)

debug = True
loglevel = debug
bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2
worker_class = "gevent"
timeout = 100

loglevel = 'warnning'

pidfile = '%s/logs/%s.pid' % (current_path, file_name)
errorlog = '%s/logs/%s_error.log' % (current_path, file_name)
accesslog = '%s/logs/%s_access.log' % (current_path, file_name)
