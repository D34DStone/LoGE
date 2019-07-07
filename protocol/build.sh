#!/bin/sh

WORKING_DIR=$(cd $(dirname "$0"); pwd -P)
echo $WORKING_DIR

if [ "$(command -v protoc)" == "" ]; then
    echo "Error: Can't find protobuf package installed."
    exit 1;
fi

for protof in $(ls | grep .proto); do
    echo "Building $protof ..."
    protoc --proto_path=$WORKING_DIR --python_out=$WORKING_DIR $protof 
done
