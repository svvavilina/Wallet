# Service gets requests from the client (here it's gateway class but it may be mobile app or web client)
# Store requests in FIFO
# Execute requests and send response to client

from queue import Queue
import logging

from wallet import Wallet
from wallet import SourceType
from request import Request
from request import Response
from request import RequestType
from request import ResponseType


class Service:
    def __init__(self, event_req):
        self.event = event_req  # Event request's been added
        self.logger = logging.getLogger('service')
        self.logger.info('Initialize Wallet')
        self.wallet = Wallet(SourceType.FILE)

        self.logger.info('Create request queue')
        self.queue = Queue()

    def get(self):
        # type: () -> Request
        self.logger.info('Get request from queue')
        return self.queue.get()

    def set(self, request):
        # type: (Request) -> None
        self.logger.info('Put request %s to queue' % request.__str__())
        self.queue.put(request)
        self.event.set()

    def process(self):
        # type: () -> Response
        self.logger.info('Start request processing')
        req = self.get()
        if self.queue.empty():
            self.event.clear()
        self.logger.info('Request to process: %s' % req.__str__())
        result = False
        if req.type is RequestType.TRANSACTION:
            result = self.wallet.req_transaction(req.body)

        response = Response(req.uid)
        if result is 0:
            response.type = ResponseType.ACK
        if result is 1:
            response.type = ResponseType.ERROR
            response.body = {'code': result,
                             'msg': self.wallet.TRANSACTION_ERROR % self.wallet.TRANSACTION_ERROR_MIN}
        if result is 2:
            response.type = ResponseType.ERROR
            response.body = {'code': result,
                             'msg': self.wallet.TRANSACTION_ERROR % self.wallet.TRANSACTION_ERROR_MAX}
        self.logger.info(response)
        return response

    def save(self):
        if self.wallet.source_type is SourceType.FILE:
            self.wallet.save_file(self.wallet.filename)
