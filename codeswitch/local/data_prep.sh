#!/bin/bash

# author: Emily Hua

sudo apt-get install flac

cp -r ../../wsj/s5/steps ../
cp -r ../../wsj/s5/utils ../

if [[ ! -e ./local ]]; then
            mkdir local/lang
fi

# Move audios to the correct directories. 
chmod 755 audio_data_prep.py
./audio_data_prep.py

# Prepare acoustic data (wav.scp, segments, utt2spk, spk2gender, text). 
chmod 755 acoustic_data_prep.py
./acoustic_data_prep.py

# Execute utils script under codeswitch directory NOT local 
cd ../
# Make the utt2spk and spk2utt files.
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt
export LC_ALL=C # set sorting mechanism 
utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/test 

utils/validate_data_dir.sh --no-feats data/train
utils/validate_data_dir.sh --no-feats data/test

echo "Acoustic Data preparation succeeded"

# Create words.txt (word symbol table) in data/train and data/test
for x in train test; do 
  cut -d ' ' -f 2- data/$x/text | sed 's/ /\n/g' | sort -u > data/$x/words.txt
done

# Create nnsilence_phones.txt and optional_silence.txt
cut -d ' ' -f 2- data/local/lang/lexicon.txt | sed 's/ /\n/g' | sort -u > data/local/lang/nonsilence_phones.txt
echo 'SIL' > data/local/lang/optional_silence.txt

utils/prepare_lang.sh data/local/lang '<oov>' data/local/ data/lang
echo "Language Data preparation succeeded"
