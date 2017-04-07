#!/bin/bash

# author: Emily Hua

sudo apt-get install flac

cp -r ../../wsj/s5/steps ../
cp -r ../../wsj/s5/utils ../

mkdir lang
mkdir local
cd local
mkdir lang

# Move audios to the correct directories. 
chmod 755 audio_data_prep.py
./audio_data_prep.py

# Prepare acoustic data (wav.scp, segments, utt2spk, spk2gender, text). 
chmod 755 acoustic_data_prep.py
./acoustic_data_prep.py

export LC_ALL=C # set sorting mechanism 
utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/test 

# Make the utt2spk and spk2utt files. Execute utils script under codeswitch directory NOT local 
cd ../
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt

utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/test 

utils/validate_data_dir.sh data/train
utils/validate_data_dir.sh data/test

echo "Acoustic Data preparation succeeded"
