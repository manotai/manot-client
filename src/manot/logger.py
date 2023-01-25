import logging
import sys

class RequestFormatter(logging.Formatter):

    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    white = '\u001b[37m'
    reset = '\u001b[0m'
    background_red = '\u001b[41m'

    def __init__(self):
        super().__init__()
        self.fmt = '%(asctime)s -- %(levelname)s: --> %(message)s'
        self.FORMATS = {
            logging.DEBUG: self.white + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.background_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="[%d/%b/%Y %H:%M:%S]")
        return formatter.format(record)


def get_stream_handler(formatter):
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    return stream_handler

def get_logger(name, formatter):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_stream_handler(formatter))
    return logger

log = get_logger(__name__, RequestFormatter())