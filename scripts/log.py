import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os


def setup_logger(app):
    formatter = Formatter("[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
    log_filename = os.path.join(app.config['APP_DIR'], 'logs/app.log')
    print log_filename
    # log_handler = TimedRotatingFileHandler('logs/foo.log', when='midnight', interval=1)
    log_handler = RotatingFileHandler(log_filename, maxBytes=1000000, backupCount=5)
    log_handler.setLevel(logging.DEBUG)
    # log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    # logwzg = logging.getLogger('werkzeug')
    # logwzg.setLevel(logging.DEBUG)
    # logwzg.addHandler(log_handler)
    app.logger.addHandler(log_handler)
