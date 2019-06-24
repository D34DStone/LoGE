import enum

class Protocol:

    class HeaderType(enum.Enum):
        REQUEST = 1
        RESPONSE = 2
        ERROR = 3


    class Errors:
        INVALID_HEADER = "INVALID_HEADER"


    @staticmethod 
    def response(str_data):
        if str_data[-1] != '\n':
            str_data += '\n'

        response = f"RESPONSE {len(str_data)}\n{str_data}"
        return response.encode()


    @staticmethod
    def error(str_err):
        response = f"ERROR {len(str_err) + 1}\n{str_err}\n"
        return response.encode()


    @staticmethod
    def parse_header(header):
        """ Takes header bytes and return touple of `Protocol.HeaderType` and `int`
        -- data type and data length respectively.
        """
        headerMap = {
            "REQUEST" : Protocol.HeaderType.REQUEST,
            "RESPONSE" : Protocol.HeaderType.RESPONSE,
            "ERROR" : Protocol.HeaderType.ERROR
        }
        header = header.decode()
        header_words = header.split()
        assert len(header_words) > 0, "Header is empty"
        data_type = headerMap[header_words[0]]
        data_size = 0 if len(header_words) == 1 else int(header_words[1])
        return data_type, data_size
