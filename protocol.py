import enum

class Protocol:

    class Header(object):
        REQUEST = "REQUEST"
        RESPONSE = "RESPONSE"
        ABORT = "ABORT"
        ERROR = "ERROR"


    class Error(object):
        INVALID_HEADER = "INVALID_HEADER"
