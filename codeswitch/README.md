# codeswitch directory description

move this `codeswitch` directory under `kaldi/egs/`
```
cp codeswitch ./kaldi/egs/
```
also put the `LDC2015S04` raw data folder under `kaldi/egs/codeswitch` 

## Table of contents
- [run.sh](#run)
  - [local](#local)
  - [calculate MER](#mer)
- [Directory Overview](#do)
  - [exp](#exp)
  - [exp_pitch](#exp_pitch)
  - [data](#data)
  - [data_v4](#data4)
  - [mfcc](#mfcc)  
- [Audio Data Description](#ad)
  - [Interview](#d2)
  - [Conversation](#d1)
- [Acoustic Data Preperation](#acoustic-prep)
  - [acoustic_data_prep.py](#adp)
  - [Create feats.scp](#feats)
  - [Create cmvn.scp](#cmvn)
  - [Validate directory](#vd)
- [Language Data Prep](#ld)
  - [Language Model](#lm)
- [Decoding](#decode)


### <a name="run"></a>run.sh
contains the main script to prepare acoustic data and create MFCC feature extractions, language model generation, tri-phone alignment, DNN and decode the system.   
to execute:
```
./run.sh
```
in `run.sh`, a shell script called `data_prep.sh` will be execuated to prepare audio and acoustic data, along with fixing and validating the directories. 

### <a name="local"></a> local
contains data preperation script, scoring script and neural networks-training script specifically designed for this task.    
within `data_prep.sh`, it calls `audio_data_prep.py` and `acoustic_data_prep.py` to prepare audio and acoustic data, along with native Kaldi script to generate `spk2utt`, sorting files and validate `data/train` and `data/test` directories.   
`data_prep.sh` also calls `lang_data_prep.py` which cleans up the transcription and prepares the lexicon. 

### <a name="mer"></a> calculate MER
If you want to use `MER_score.sh` to calculate char or word level MER (with Chinese and English Ins, Subs, Del displayed), please see the following example for execution:
```
cd local
chmod +x MER_score.py
./MER_score.py tri2 /data/lang True
./MER_score.py nnet2_online/nnet_a_gpu_baseline /data/lang False
```
`MER_score.py` takes in three arguments:
1. model dir
2. lang dir
3. True for using char based calculator, False for using word based calculation  

sampe output:
![alt text](https://github.com/yh1008/speech-to-text/blob/master/codeswitch/local/assets/MER_output.png)

### path.sh 
tells where to find kaldi binary `. ./path.sh` is executed on all shell script to set the kaldi environment variable. 
to manually check if it is setted, use command
```
echo $KALDI_ROOT
```
## <a name="do"></a>Directory Overview  
### <a name="exp"></a>exp
`tri2`(LDA) and `tri22` (LDA+LDA) model created using language data v2(eng uppercase, merge SIL, eng oov not reduced, remains 1244/9520)      

### <a name="exp_pitch"></a>exp_pitch
 model created using language data v4(eng uppercase, merge SIL, eng oov reduced to ~800/9520)  

### <a name="data"></a>data
`data` folder created by `data_prep.sh` using language data v2(eng uppercase, merge SIL, eng oov not reduced, remains 1244/9520)   

### <a name="data4"></a>data_v4
`data` folder created by `data_prep.sh` using language data v4(eng uppercase, merge SIL, eng oov reduced to ~800/9520)  

### <a name="mfcc"></a>mfcc
stores `mfcc`(Mel Frequency Cepstral Coefficents) feature and `cmvn` (Cepstral Mean and Variance Normalization) features 

## Acoustic Data Preperation
### <a name="ad"></a> Audio Data  
#### <a name="d2"></a> For seame_d2/data/interview:    
there are 95 speaker-id in total (e.g. NI01MAX). Technically format of `01MA` is sufficient for identifying any unique speaker in our audios, but to make the utterance-id, recording-id and speaker-id aligned for Kaldi to process, I decide to make the entire prefix (e.g. NI01MAX) of recording-id (e.g. NI01MAX_0101.flac) my speaker-id.   

description of the speaker-id NI01MA: N is recording location, I stands for `i`nterview style, 01 is spearker identity, M for gender (M for male, F for female), A for nationality (A is Malaysian, B is Singaporean)     

test set contains 10 speaker id: 'UI08MAZ', 'NI67MBQ', 'UI03FAZ', 'NI45FBP', 'NI55FBP', 'NI42FBQ', 'NI01MAX', 'UI29FAZ', 'NI29MBP', 'NI44MBQ'

train set contains 85 speaker id: 'NI28MBP', 'UI01FAZ', 'NI25MBQ', 'UI07FAZ', 'UI23FAZ', 'UI17FAZ', 'NI02FAX', 'NI27MBQ', 'NI09FBP', 'NI31FBP', 'UI04FAZ', 'UI12FAZ', 'UI18MAZ', 'NI46FBQ', 'UI28FAZ', 'UI02FAZ', 'NI56MBX', 'NI62MBQ', 'NI14MBP', 'NI59FBQ', 'NI37MBP', 'NI63MBP', 'NI26FBP', 'NI21MBQ', 'NI61FBP', 'UI20MAZ', 'NI41MBP', 'NI52MBQ', 'NI65MBP', 'NI18MBP', 'NI57FBQ', 'UI06MAZ', 'NI58FBP', 'NI49MBP', 'NI60MBP', 'NI50FBQ', 'UI05MAZ', 'NI54FBQ', 'NI51MBP', 'NI66MBQ', 'NI35FBP', 'NI05MBQ', 'NI10FBP', 'UI10FAZ', 'NI39FBP', 'NI53FBP', 'NI03FBX', 'NI33MBP', 'UI27FAZ', 'NI47MBP', 'NI23FBQ', 'NI36MBQ', 'UI25FAZ', 'NI15FBQ', 'NI32FBQ', 'NI48FBQ', 'NI12MAP', 'UI22MAZ', 'NI24MBP', 'UI26MAZ', 'UI15FAZ', 'UI09MAZ', 'NI30MBQ', 'NI16FBP', 'UI14MAZ', 'NI17FBQ', 'NI43FBP', 'NI04FBX', 'NI13MBQ', 'UI24MAZ', 'NI34FBQ', 'NI06FBP', 'NI22FBP', 'UI11FAZ', 'UI16MAZ', 'NI11FBP', 'NI08FBP', 'NI07FBQ', 'UI19MAZ', 'NI20MBP', 'NI64FBQ', 'UI13FAZ', 'NI19MBQ', 'UI21MAZ', 'NI40FBQ'

#### <a name="d1"></a> For seame_d1/data/conversation:  
there are 64 speaker-id in total (e.g. NC16FBQ). The original recording naming format is 08NC16FBQ_0101 where 08 is the conversation group, C stands for `c`oncersation, 0101 stands for the first part of the first recording of this speaker. Since the same speaker (e.g. NC16FBQ) can end up in multiple conversation group and Kaldi strictly requires speaker-id to be the prefix of utterance-id and recording-id, I rename this kind of recordings to NC16FBQ_080101 instead. 

test set contains 4 speaker id: 'NC01FB', 'NC02FB','NC11MA', 'NC12MA'

train set contains 60 speaker id: 'NC41MBP', 'NC22MBQ', 'NC40FBQ', 'NC53MBP', 'NC04FBY', 'NC48FBP', 'NC14FBQ', 'NC37MBP', 'NC47MBQ', 'NC35FBP', 'NC09FAX', 'NC33FBP', 'NC50FBP', 'NC15MBP', 'NC31FBP', 'NC44MBQ', 'NC59MAX', 'NC07FBX', 'NC57FBX', 'NC38FBQ', 'NC47MBP', 'NC27MBP', 'NC26MBQ', 'NC39MBP', 'NC23FBP', 'NC19MBP', 'NC20MBQ', 'NC28MBQ', 'NC49FBQ', 'NC06FAY', 'NC58FAY', 'NC52FBQ', 'NC08FBY', 'NC13MBP', 'NC42MBQ', 'NC30MBQ', 'NC43FBQ', 'NC03FBX', 'NC32FBQ', 'NC29FBP', 'NC61FBQ', 'NC56MBP', 'NC18MBQ', 'NC05FAX', 'NC25MBP', 'NC10MAY', 'NC46FBQ', 'NC43FBP', 'NC50XFB', 'NC16FBQ', 'NC35FBQ', 'NC34FBQ', 'NC51MBP', 'NC24FBQ', 'NC17FBP', 'NC21FBP', 'NC54FBQ', 'NC60FBQ', 'NC45MBP', 'NC36MBQ'



### <a name="acoustic-prep"></a> Acoustic Data
make sure to execute `. ./path.sh` before running any command to set the Kaldi environmental variable 

Upon recreating utterance id based on start and end time from each recording, we end up with 54594 (46578 based on filtered transcript) utterances:
1. there are 50457 (43186 based on filtered transcript) utterances in train set  
2. there are 4137 (3392 based on filtered transcript) utterances in test set    

In real feature extraction: (the following stats is depreciated, the `tri2` and `tri22` are in fact created using `43186` in `train` and `3392` utterances in `test`)
1. calling fix_data_dir.sh: kept 49897 utterances out of 50457 (speaker NC50XFB was filtered out cause its gender is unknown) 
2. fix_data_dir.sh: kept all 4137 utterances.

#### <a name="adp"></a> Acoustic_data_prep.py
files I code the `acoustic_data_prep.py` to create:   
- [x] utt2spk  
- [x] text   
- [x] wav.scp  
- [x] spk2gender
- [x] segments   

files I called the kaldi script to create:
- [x] spk2utt
- [x] feats.scp  
- [x] cmvn.scp  

#### <a name="feats"></a> feats.scp
**feats.scp** points tothe extracted features-MFCC features. The pattern is \<utterance-id> \<extended-filename-of-features> 
```
$ less feats.scp | head -2

NI02FAX_0101_0055711_0060021 /home/yh2901/kaldi/egs/codeswitch/mfcc/raw_mfcc_train.1.ark:29
```
The above (extended file name) means, open the "archive" file /home/yh2901/kaldi/egs/codeswitch/mfcc/raw_mfcc_train.1.ark:29, fseek() to position 24, and read the data that is there.   
To create this feats.scp, type 
```
steps/make_mfcc.sh --nj 8 data/train exp/make_mfcc/train mfcc
steps/make_mfcc.sh --nj 8 data/test exp/make_mfcc/test mfcc
```
now my mfcc directory contains 
```
 tree mfcc
mfcc
├── raw_mfcc_test.1.ark
├── raw_mfcc_test.1.scp
├── raw_mfcc_test.2.ark
├── raw_mfcc_test.2.scp
├── raw_mfcc_test.3.ark
├── raw_mfcc_test.3.scp
├── raw_mfcc_test.4.ark
├── raw_mfcc_test.4.scp
├── raw_mfcc_test.5.ark
├── raw_mfcc_test.5.scp
├── raw_mfcc_test.6.ark
├── raw_mfcc_test.6.scp
├── raw_mfcc_test.7.ark
├── raw_mfcc_test.7.scp
├── raw_mfcc_test.8.ark
├── raw_mfcc_test.8.scp
├── raw_mfcc_train.1.ark
├── raw_mfcc_train.1.scp
├── raw_mfcc_train.2.ark
├── raw_mfcc_train.2.scp
├── raw_mfcc_train.3.ark
├── raw_mfcc_train.3.scp
├── raw_mfcc_train.4.ark
├── raw_mfcc_train.4.scp
├── raw_mfcc_train.5.ark
├── raw_mfcc_train.5.scp
├── raw_mfcc_train.6.ark
├── raw_mfcc_train.6.scp
├── raw_mfcc_train.7.ark
├── raw_mfcc_train.7.scp
├── raw_mfcc_train.8.ark
└── raw_mfcc_train.8.scp

0 directories, 32 files
```
#### <a name="cmvn"></a> cmvn.scp 
to compute **cmvn.scp** which contains statistics for cepstral mean and variance normalization, indexed by speaker, type
```
$ steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train mfcc
```
generates cmvn.scp in data/train and data/test
```
$ less cmvn.scp | head -2
NI02FAX /home/yh2901/kaldi/egs/codeswitch/mfcc/cmvn_train.ark:8
NI03FBX /home/yh2901/kaldi/egs/codeswitch/mfcc/cmvn_train.ark:255
```
#### <a name="vd"></a> validate directory
validate the data/train and data/test after generating utt2spk file:
- [x] utils/validate_data_dir.sh --no-feats data/train 
- [x] utils/validate_data_dir.sh --no-feats data/test 

validate the data/train and data/test after generating feats.scp file:
- [x] utils/validate_data_dir.sh data/train 
- [x] utils/validate_data_dir.sh data/test 

fix the sorting error, use the following command:
```
utils/fix_data_dir.sh data/train 
```
## <a name="ld"></a>Language Data Preparation

### 1. Get word list
#### Folder: data/train, data/test
#### File created: words.txt
#### File content: all the unique words in text
```
cut -d ' ' -f 2- text | sed 's/ /\n/g' | sort -u > words.txt
```

### 2. Filter lexicon
#### Folder: data/local/lang
#### File created: lexicon.txt
#### File content: the pronunciation (phones) of words that appear in the data
Using python script

### 3. Create phone list
#### Folder: data/local/lang
#### File created: nonsilence_phone.txt, silence_phone.txt, optional_silence.txt
#### File content: the range of phones
silence_phone.txt is from python script
```
cut -d ' ' -f 2- lexicon.txt | sed 's/ /\n/g' | sort -u > nonsilence_phones.txt
echo 'SIL' > optional_silence.txt
```

### 4. Generate other files
#### Folder: codeswitch
#### File created: phones (folder), oov.txt, L.fst
#### File content: 
```
cd codeswitch
utils/prepare_lang.sh data/local/lang '<oov>' data/local/ data/lang
```
### 5. Install srilm to build the ARPA language model 

you can download this srilm-1.7.2.tar.gz from [SRILM](http://www.speech.sri.com/projects/srilm/download.html) by filling out the download form (I uploaded this gz file to Git, but received an warning cause it exceeds 50MB limit. If you observe that this gz is currupted, go download it directly from the url linked above). And then copy this file to `kaldi/tools` and name it `srilm.tgz`. After that, execute `install_srilm.sh`
```
cp srilm-1.7.2.tar.gz ~/kaldi/tools/srilm.tgz
cd kaldi/tools
./install_srilm.sh
```
build the language model using the following script: 

```
cd ~/kaldi/egs/codeswitch
loc=`which ngram-count`;
   if [ -z $loc ]; then
       if uname -a | grep 64 >/dev/null; then
               sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
       else
               sdir=$KALDI_ROOT/tools/srilm/bin/i686
         fi
       if [ -f $sdir/ngram-count ]; then
                echo "Using SRILM language modelling tool from $sdir"
                export PATH=$PATH:$sdir
   else
           echo "SRILM toolkit is probably not installed.
           Instructions: tools/install_srilm.sh"
      exit 1
   fi
fi
mkdir data/local/tmp
ngram-count -order 3 -write-vocab data/local/tmp/vocab-full.txt -wbdiscount -text data/local/corpus.txt -lm data/local/tmp/lm.arpa
```

### <a name="lm"></a> 6. create G.fst using the ARPA language model
`G.fst` is an acceptor (i.e. input and output symbols are identical on each arc) with words as its symbols. The exception is the disambiguation symbol #0 which only appears on the input side. 
```
 lang=data/lang
 local=data/local
 arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst
```
Here we used `disambig-symbol=#0` to make the grammar transducer(G) determinizable. The effect of this omission was that the back-off arcs in the G.fst being cut-off, leading to a highly non-stochastic LG cascade with a very spiky distribution over the allowed word sequences and hence the higher WER [source](http://vpanayotov.blogspot.com/2012/06/kaldi-decoding-graph-construction.html)  
`#0` is used for epsilon on the input of G.fst. `episolon` ( `<eps>` ) is a special symbol, meaning "there is no symbol on this arc". `eps2disambig.pl` converts all episolon input labels to special symbol `#0`. I checked, in our lexicon there is no `#0`, so this symbol won't be mistaken as a word. [source](http://kaldi-asr.org/doc/graph_recipe_test.html)

## <a name="decode"></a>Decoding Phase
### 1. Make sure to install portaudio successfully
```
cd /kaldi/tools
./install_portaudio.sh
cd /kaldi/src
make ext -j 8
```

### 2. Copy egs/voxforge/online_demo to kaldi/egs/codeswitch/
```
cp -r /kaldi/egs/voxforge/online_demo /kaldi/egs/codeswitch/
```

### 3. Within codeswitch/online_demo
```
mkdir online-data
cd online-data
mkdir audio && mkdir models
cd models
mkdir mono
```

#### The structure looks like:
```
codeswitch/
├── online_demo
│   ├── online-data
│   │   └── models
│   │       ├── mono
│   │       │   ├── final.mdl
│   │       │   ├── words.txt
│   │       │   ├── HCLG.fst
│   │   └── audio
│   │       ├── test.wav
│   │       ├── test.wav.trn
```

#### Copy final.mdl to models/mono; copy graph_word/words.txt to models/mono; copy graph_word/HCLG.fst to models/mono;
#### Copy a wav and its transcription into audio folder
 
### 4. Run the script
```
cd kaldi/egs/codeswitch/online_demo
./run.sh
```

### Accuracy Recorder

Case-inconsistant: WER 85% on tri2 LDA+MLLT  
Case-consistant, 200+SIL: WER 66% on tri2 LDA+MLLT, WER 56-60% on DNN online/nnet2_baseline.sh

