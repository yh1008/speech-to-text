#!/bin/bash
git clone https://github.com/kaldi-asr/kaldi.git
cd kaldi/tools
sudo apt-get install  zlib1g-dev automake autoconf libtool subversion
sudo apt-get install libatlas3-base
sudo ln -s -f bash /bin/sh
extras/check_dependencies.sh
make -j 8
extras/install_irstlm.sh
cd ../src
./configure
make depend -j 8
make -j 8
