#!/bin/bash

# install gcc and make packages
sudo apt-get install build-essential

# install protocol buffers
sudo apt-get install libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python3-protobuf

# install other required libs
sudo apt-get install libcap-dev libnl-3-dev libnet-dev

# install pkg-config to check on build library dependencies
sudo apt-get install pkg-config

