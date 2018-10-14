# Simple client to get data to manipulate
# Collect and form request
# Send request to the wallet service
# Should be changed to the mobile app or web client

import logging
import threading

from service import Service
from request import Request
from request import Response
from request import RequestType
from request import ResponseType
from request import RequestTransaction


class Gateway:
    # Add another menu options
    MENU_ITEMS = {1: 'Transaction',
                  2: 'Exit'}

    TIMEOUT = 60000

    def __init__(self):
        self.logger = logging.getLogger("gateway")
        self.stop = False

        self.event_request = threading.Event()
        self.logger.info('Initialize Service')
        self.service = Service(self.event_request)
        self.logger.debug('Initialize wallet thread')
        self.th_service = threading.Thread(target=self.request_loop)
        self.id = 'client0001'
        self.logger.info('Gateway client id %s' % self.id)

    def __str__(self):
        str_menu = 'Menu items:\n'
        for item in self.MENU_ITEMS:
            str_menu += '\t%d - %s\n' % (item, self.MENU_ITEMS[item])
        return str_menu

    def _transaction(self):
        self.logger.info('Start transaction data input')
        print('Input transaction parameters')
        request = Request(self.id, RequestType.TRANSACTION)
        user_from = input('From user: ')
        user_to = input('To user: ')
        value = input('Amount: ')

        request.body[RequestTransaction.FROM] = user_from
        request.body[RequestTransaction.TO] = user_to
        request.body[RequestTransaction.VALUE] = int(value)

        self.logger.info('Transaction request: ' + request.__str__())
        self.service.set(request)

    def _quite(self):
        print('\tGoodbye')

    def _read_item(self):
        try:
            mode = int(input('Item number:\t'))
            if mode is 1:
                self._transaction()
            elif mode is 2:
                self._quite()
                return False
            else:
                raise ValueError
            return True
        except ValueError:
            print('Not a menu item')
            return True

    def request_loop(self):
        while not self.stop:
            print(self.service.process())  # Get and proceed response
            self.service.event.wait()

    def session(self):
        self.logger.debug('Start wallet thread')
        self.th_service.start()

        print('Welcome')
        result = True
        while result:
            print(self)
            result = self._read_item()
        self.stop = True
        self.service.event.set()
        self.service.save()
        self.logger.debug('Wait for thread to join')
        self.th_service.join(self.TIMEOUT)

