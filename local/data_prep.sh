#!/bin/bash

sudo apt-get install flac

cp -r ../wsj/s5/steps ./
cp -r ../wsj/s5/utils ./

./audio_data_prep.py
./acoustic_data_prep.py

export LC_ALL=C
utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/test 

../utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
../utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt

mkdir conf
cp ../timit/s5/conf/mfcc.conf ./conf
