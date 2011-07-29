import logging
from django.conf import settings

def getlogger():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S') 
    
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger

# def debug(msg):
#     logger = getlogger()
#     logger.debug(msg)


def info(msg):
    logger = getlogger()
    logger.info(msg)


def warning(msg):
    logger = getlogger()
    logger.warning(msg)

# logger=getlogger()