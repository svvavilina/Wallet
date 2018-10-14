# Request/Response structures file


from enum import Enum, unique
import datetime


@unique
class RequestType(Enum):
    # Add request type e.g. get wallet balance
    TRANSACTION = 0


class Request:
    # May be changed
    # e.g. Add location or security keys
    def __init__(self, uid, req_type, body={}):
        # type: (str,RequestType,dict) -> None
        self.uid = uid
        self.timestamp = datetime.datetime.now()
        self.type = req_type
        self.body = body

    def __str__(self):
        return """UID : {req.uid}
        TIMESTAMP : {req.timestamp}
        TYPE : {req.type}
        BODY : {req.body}""".format(req=self)


class RequestTransaction:
    # request transaction body keys
    FROM = 'from'
    TO = 'to'
    VALUE = 'value'


#May be created classes with body keys for another request types


@unique
class ResponseType(Enum):
    # Add response type
    NONE = -1
    ACK = 0
    ERROR = 1


class Response:
    # Add all necessary field for response
    def __init__(self, uid, res_type = ResponseType.NONE, body={}):
        # type: (str,ResponseType,dict) -> None
        self.uid = uid
        self.timestamp = datetime.datetime.now()
        self.type = res_type
        self.body = body

    def __str__(self):
        return """UID : {res.uid}
        TIMESTAMP : {res.timestamp}
        TYPE : {res.type}
        BODY : {res.body}""".format(res=self)