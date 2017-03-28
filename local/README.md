# Data Preperation

### Audio Data  

For seame_d2/data/interview:    
there are 94 unique speakers in total  
for speaker id 01MA: 01 is spearker identity, M for gender (M for male, F for female), A for nationality (A is Malaysian, B is Singaporean)     

test set contains speaker id: '01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB'   

train set contains speaker id: '37MB', '23FB', '07FB', '09FB', '19MA', '04FA', '06FB', '57FB', '25FA', '64FB', '36MB', '28MB', '23FA', '56MB', '20MA', '43FB', '25MB', '30MB', '52MB', '21MB', '26FB', '22FB', '05MA', '17FB', '08FB', '22MA', '58FB', '12FA', '46FB', '15FA', '17FA', '13FA', '07FA', '21MA', '50FB', '61FB', '14MA', '19MB', '03FB', '66MB', '62MB', '04FB', '10FB', '06MA', '13MB', '11FB', '41MB', '48FB', '26MA', '53FB', '14MB', '40FB', '24MA', '27FA', '28FA', '34FB', '63MB', '60MB', '35FB', '18MA', '47MB', '12MA', '65MB', '02FA', '27MB', '33MB', '59FB', '09MA', '31FB', '39FB', '15FB', '16MA', '24MB', '51MB', '05MB', '32FB', '54FB', '01FA', '18MB', '49MB', '20MB', '11FA', '10FA', '16FB'

### Acoustic Data
make sure to execute . ./path.sh before running any command to set the Kaldi environmental variable 

Upon recreating utterance id based on start and end time from each recording, we end up with 40712 utterances:
1. there are 37060 utterances in train set  
2. there are 3652 utterances in test set  

files I manually created:   
- [x] utt2spk  
- [x] text   
- [x] wav.scp  
- [x] spk2gender
- [x] segments   

files I called the kaldi script to create:
- [x] spk2utt
- [x] feats.scp  
- [x] cmvn.scp  

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
