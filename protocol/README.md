## Internal LoGE network protocol

### Basic principles

* Network protocol implements client-server architecture

* Every message containts: 
    1) Header which describes what is it
    2) Size of data in bytes
    3) Binary data 

* Every data-schema described in .proto files

Regular message may look like that:
```
AUTH_REQUEST 201
*Here goes 201 byte of binary data*
```

### Client-server interaction blueprint

Authorization
```
AUTH\_REQUEST 
AUTH\_RESPONSE
```

Starting game
```
START\_REQUEST
START\_RESPONSE
```

Getting character
```
CHARACTER\_REQUEST
CHARACTER\_RESPONSE
```


