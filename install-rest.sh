#!/bin/bash

sudo  apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-numpy python3-scipy
pip3 install h5py
sudo pip3 install --upgrade --no-deps git+git://github.com/Theano/Theano.git
sudo pip3 install tensorflow
sudo pip3 install keras
sudo apt-get -y install ipython ipython-notebook
sudo -H pip install jupyter
