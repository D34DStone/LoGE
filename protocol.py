class Header(object):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    ABORT = "ABORT"
    ERROR = "ERROR"


class Error(object):
    INVALID_HEADER = "INVALID_HEADER"
    SERIALIZE_ERROR = "SERALIZATION_ERROR"
    WRONG_REQUEST = "WRONG_REQUEST"
    
def make_request(datatype, data):
    if isinstance(data, str):
        data = data.encode()

    return f"{datatype} {len(data)}\n".encode() + data

def parse_header(header):
    """Returns type and size of data. 
    """
    header = header.decode()
    header_words = header.split()
    assert len(header_words) > 0, "Header is empty"
    data_type = header_words[0]
    data_size = 0 if len(header_words) == 1 else int(header_words[1])
    return data_type, data_size
