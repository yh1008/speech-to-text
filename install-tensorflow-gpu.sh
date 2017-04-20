!/bin/bash

sudo tar -xvf cudnn-8.0-linux-x64-v5.0-ga.tgz -C /usr/local
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
# makes sure you add the following path in ~/.profile 
# export CUDA_HOME=/usr/local/cuda
# export DYLD_LIBRARY_PATH="$DYLD_LIBRARY_PATH:$CUDA_HOME/lib"
# export PATH="$CUDA_HOME/bin:$PATH"

sudo apt-get install python-pip python-dev
pip install --upgrade pip

sudo apt-get install software-properties-common swig 
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
echo "deb http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list 
curl https://storage.googleapis.com/bazel-apt/doc/apt-key.pub.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install bazel

git clone https://github.com/tensorflow/tensorflow
cd tensorflow
./configure
# install tensorflow with openCL no
# cuda version 8.0
# cudnn version 5

bazel build -c opt //tensorflow/tools/pip_package:build_pip_package
bazel build -c opt --config=cuda //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
sudo pip install /tmp/tensorflow_pkg/tensorflow-1.1.0rc2-cp27-cp27mu-linux_x86_64.whl
# depends on distribution on your system, to check which .whl it is, type ls -l /tmp/tensorflow_pkg
