import logging
import os

from logging.handlers import RotatingFileHandler
from os.path import exists, join

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    target_dir = 'logs'
    if not exists(target_dir):
        os.makedirs(target_dir)

    handler = RotatingFileHandler(join(target_dir, "find-a-flat-bot.log"), encoding='utf-8', maxBytes=1024*1024*10, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


setup_logger()
