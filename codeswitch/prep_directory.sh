# from http://pages.jh.edu/~echodro1/tutorial/kaldi/kaldi-training.html
cd codeswitch
ln -s ../wsj/s5/steps .
ln -s ../wsj/s5/utils .
ln -s ../../src .

cp ../wsj/s5/path.sh .

# since the codeswitch directory is a level higher than wsj/s5, we need to edit the path.sh file

vim path.sh 
# Press i to insert; esc to exit insert mode; ‘:wq’ to write and quit; ‘:q’ to quit normally; ‘:q!’ to quit forcibly (without saving)
# Change the path line in path.sh from: export KALDI_ROOT='pwd'/../../.. to export KALDI_ROOT='pwd'/../..

cd codeswitch
mkdir exp
mkdir conf
mkdir data

cd data
mkdir train
mkdir lang
mkdir local

cd local
mkdir lang
