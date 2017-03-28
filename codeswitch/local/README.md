# Data Preperation

### Audio Data  

For seame_d2/data/interview:    
there are 95 speaker-id in total (e.g. NI01MAX). Technically format of `01MA` is sufficient for identifying any unique speaker in our audios, but to make the utterance-id, recording-id and speaker-id aligned for Kaldi to process, I decide to make the entire prefix (e.g. NI01MAX) of recording-id (e.g. NI01MAX_0101.flac) my speaker-id.   

description of the speaker-id NI01MA: N is recording location, I stands for `i`nterview style, 01 is spearker identity, M for gender (M for male, F for female), A for nationality (A is Malaysian, B is Singaporean)     

test set contains 10 speaker id: ['UI08MAZ', 'NI67MBQ', 'UI03FAZ', 'NI45FBP', 'NI55FBP', 'NI42FBQ', 'NI01MAX', 'UI29FAZ', 'NI29MBP', 'NI44MBQ'] 

train set contains 85 speaker id: ['NI28MBP', 'UI01FAZ', 'NI25MBQ', 'UI07FAZ', 'UI23FAZ', 'UI17FAZ', 'NI02FAX', 'NI27MBQ', 'NI09FBP', 'NI31FBP', 'UI04FAZ', 'UI12FAZ', 'UI18MAZ', 'NI46FBQ', 'UI28FAZ', 'UI02FAZ', 'NI56MBX', 'NI62MBQ', 'NI14MBP', 'NI59FBQ', 'NI37MBP', 'NI63MBP', 'NI26FBP', 'NI21MBQ', 'NI61FBP', 'UI20MAZ', 'NI41MBP', 'NI52MBQ', 'NI65MBP', 'NI18MBP', 'NI57FBQ', 'UI06MAZ', 'NI58FBP', 'NI49MBP', 'NI60MBP', 'NI50FBQ', 'UI05MAZ', 'NI54FBQ', 'NI51MBP', 'NI66MBQ', 'NI35FBP', 'NI05MBQ', 'NI10FBP', 'UI10FAZ', 'NI39FBP', 'NI53FBP', 'NI03FBX', 'NI33MBP', 'UI27FAZ', 'NI47MBP', 'NI23FBQ', 'NI36MBQ', 'UI25FAZ', 'NI15FBQ', 'NI32FBQ', 'NI48FBQ', 'NI12MAP', 'UI22MAZ', 'NI24MBP', 'UI26MAZ', 'UI15FAZ', 'UI09MAZ', 'NI30MBQ', 'NI16FBP', 'UI14MAZ', 'NI17FBQ', 'NI43FBP', 'NI04FBX', 'NI13MBQ', 'UI24MAZ', 'NI34FBQ', 'NI06FBP', 'NI22FBP', 'UI11FAZ', 'UI16MAZ', 'NI11FBP', 'NI08FBP', 'NI07FBQ', 'UI19MAZ', 'NI20MBP', 'NI64FBQ', 'UI13FAZ', 'NI19MBQ', 'UI21MAZ', 'NI40FBQ']


### Acoustic Data
make sure to execute `. ./path.sh` before running any command to set the Kaldi environmental variable 

Upon recreating utterance id based on start and end time from each recording, we end up with 40712 utterances:
1. there are 37060 utterances in train set  
2. there are 3652 utterances in test set    

In real feature extraction:  
1. calling fix_data_dir.sh: kept 36826 utterances out of 36940
2. fix_data_dir.sh: kept 3455 utterances out of 3652  

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
