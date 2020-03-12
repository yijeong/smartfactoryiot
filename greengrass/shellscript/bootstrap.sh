#!/bin/bash

sudo apt-get update


sudo apt-get -y install python3-pip
sudo python3 -m pip install AWSIoTPythonSDK
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 3
sudo update-alternatives --config python


sudo apt-get -y install build-essential
sudo apt-get -y install cmake
sudo apt-get -y install zlibc
sudo apt-get -y install libssl-dev
sudo apt-get -y install unzip
# 폴더 생성
mkdir ~/dependencies
cd ~/dependencies

# Boost dependency 파일 설치 
wget https://dl.bintray.com/boostorg/release/1.69.0/source/boost_1_69_0.tar.gz -O /tmp/boost.tar.gz
sudo tar xzvf /tmp/boost.tar.gz
cd boost_1_69_0
./bootstrap.sh
sudo ./b2 install

# Protobuf dependency 파일 설치 
cd ~/dependencies
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.tar.gz -O /tmp/protobuf-all-3.6.1.tar.gz
sudo tar xzvf /tmp/protobuf-all-3.6.1.tar.gz
cd protobuf-3.6.1
sudo mkdir build
cd build
sudo cmake ../cmake
sudo make
sudo make install


# Catch2 test framework 설치 
cd ~/dependencies
sudo git clone https://github.com/catchorg/Catch2.git
cd Catch2
sudo mkdir build
cd build
sudo cmake ../
sudo make
sudo make install