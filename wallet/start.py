import logging.config
from gateway import Gateway

if __name__ == '__main__':
    logging.config.fileConfig('config/logging.conf')
    gateway = Gateway()
    gateway.session()