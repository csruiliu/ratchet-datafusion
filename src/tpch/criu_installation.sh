#!/bin/bash

# install gcc and make packages
sudo apt-get install -y build-essential

# install protocol buffers
sudo apt-get install -y libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python3-protobuf

# install other required libs
sudo apt-get install -y libcap-dev libnl-3-dev libnet-dev

# install pkg-config to check on build library dependencies
sudo apt-get install -y pkg-config

cd /tank/local/ruiliu

wget https://github.com/checkpoint-restore/criu/archive/refs/tags/v3.17.1.tar.gz

tar -xvf v3.17.1.tar.gz

cd /tank/local/ruiliu/criu-3.17.1

make
