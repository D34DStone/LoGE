## Internal LoGE network-protocol

### Basic principles

* Protocol implements client-sever architecure
* Every package has header, size of data and data itself

Regular request from the client may look like that:
```
REQUEST 123
*binary data with length 123*
```

Response from the server:
```
RESPONSE 456
*binary data with length 456*
```

Error from the server:
```
ERROR 15
*text description of the error*
```

### Header table

| Header    | Sender    |
| --------- | --------- |
| REQUEST   | client    |
| PING      | client    | 
| RESPONSE  | server    | 
| ERROR     | server    |
| ABORT     | server    | 


### Errors 
* INVALID\_HEADER
* SERIALIZE\_ERROR
* WRONG\_REQUQEST # if client sent wrong data
* FORBIDDEN\_REQUEST # if server hasn't authrorized
