# Wallet:
# Initialize wallet service with stored values (choose datasource or easy add it)
# Store values in cache (dictionary is not the best chose for big amount of entries)

import configparser
import logging
import json
from enum import Enum, unique

from request import RequestTransaction


@unique
class SourceType(Enum):
    # Add datasource key e.g. database
    # Obviously such apps better use with db as storage
    # Load from db and store in cache e.g. Redis
    FILE = 0


class Wallet:
    _CONFIG_TRANSACTION = 'TRANSACTION'
    _CONFIG_TRANSACTION_MAX = 'max_value'

    TRANSACTION_ERROR = 'Unable to perform transaction: %s'
    TRANSACTION_ERROR_MIN = 'insufficient funds'
    TRANSACTION_ERROR_MAX = 'max funds limit exceeded'
    TRANSACTION_ERROR_USER = 'src and/or dst user is not exist'

    def __init__(self,source_type):
        # type: (SourceType) -> None
        self.logger = logging.getLogger('wallet')
        self.source_type = source_type
        self._load_config()

        self.data: dict  # Specify load data type
        # Load from specified datasource
        if source_type is SourceType.FILE:
            self.logger.info('Datasource type : file')
            self.filename = 'data.json'
            self.data = self.load_from_file(self.filename)
            self.logger.debug(self.data)

    def _load_config(self):
        self.logger.info('Load wallet configuration')
        config = configparser.ConfigParser()
        config.read('config/settings.ini')

        self.logger.info('Configuration file sections :' + config.sections().__str__())

        if config.has_option(self._CONFIG_TRANSACTION, self._CONFIG_TRANSACTION_MAX):
            self.max = int(config[self._CONFIG_TRANSACTION][self._CONFIG_TRANSACTION_MAX])
        self.logger.info('Max allowed value %d' % self.max)

    def load_from_file(self, filename):
        self.logger.info('Load wallet data from the file: %s' % filename)
        with open(filename) as file:
            return json.load(file)

    def save_file(self, filename):
        self.logger.info('Store data to the file: %s' % filename)
        with open(filename, 'w') as file:
            json.dump(self.data, file)

    def req_transaction(self, body):
        '''
        Return value:
        0 - OK
        1 - insufficient funds
        2 - max funds limit exceeded
        :param body: dict
        :return: int
        '''
        self.logger.info('Start transaction')
        _from = body[RequestTransaction.FROM]
        _to = body[RequestTransaction.TO]
        _value = body[RequestTransaction.VALUE]

        if _from not in self.data or _to not in self.data:
            self.logger.info(self.TRANSACTION_ERROR % self.TRANSACTION_ERROR_USER)
            self.logger.debug(self.data)
            self.logger.debug('_from: %s, _to: %s' % (_from, _to))
            return False

        if self.data[_from] < _value:
            self.logger.info(self.TRANSACTION_ERROR % self.TRANSACTION_ERROR_MIN)
            self.logger.debug('Available: %d, required: %d' % (self.data[_from], _value))
            return False

        if self.data[_to] > self.max:
            self.logger.info(self.TRANSACTION_ERROR % self.TRANSACTION_ERROR_MAX)
            self.logger.debug('Available: %d, max: %d' % (self.data[_to], self.max))
            return False

        self.data[_from] -= _value
        self.data[_to] += _value

        self.logger.info('Transaction success')
        self.logger.debug(self.data)

        return True

    # Add another transactions processing methods here
