# Data Preperation

### Audio Data  

For seame_d2/data/interview:    
there are 94 unique speakers in total  
for speaker id 01MA: 01 is spearker identity, M for gender (M for male, F for female), A for nationality (A is Malaysian, B is Singaporean)     

test set contains speaker id: '01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB'   

train set contains speaker id: '37MB', '23FB', '07FB', '09FB', '19MA', '04FA', '06FB', '57FB', '25FA', '64FB', '36MB', '28MB', '23FA', '56MB', '20MA', '43FB', '25MB', '30MB', '52MB', '21MB', '26FB', '22FB', '05MA', '17FB', '08FB', '22MA', '58FB', '12FA', '46FB', '15FA', '17FA', '13FA', '07FA', '21MA', '50FB', '61FB', '14MA', '19MB', '03FB', '66MB', '62MB', '04FB', '10FB', '06MA', '13MB', '11FB', '41MB', '48FB', '26MA', '53FB', '14MB', '40FB', '24MA', '27FA', '28FA', '34FB', '63MB', '60MB', '35FB', '18MA', '47MB', '12MA', '65MB', '02FA', '27MB', '33MB', '59FB', '09MA', '31FB', '39FB', '15FB', '16MA', '24MB', '51MB', '05MB', '32FB', '54FB', '01FA', '18MB', '49MB', '20MB', '11FA', '10FA', '16FB'

### Acoustic Data

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
-[x] spk2utt
feats.scp  
cmvn.scp  


error:
utils/validate_data_dir.sh: file data/train/utt2spk is not in sorted order or has duplicates  
needs to be fixed! 
```
utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh: file data/train/utt2spk is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/spk2utt is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/text is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/segments is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/wav.scp is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/spk2gender is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: filtered data/train/segments from 36990 to 36940 lines based on filter /tmp/kaldi.VKzR/recordings.
utils/fix_data_dir.sh: filtered data/train/wav.scp from 193 to 192 lines based on filter /tmp/kaldi.VKzR/recordings.
- data/train/utt2spk differ: char 3299, line 98
utt2spk is not in sorted order (fix this yourself)
```
[possible solutions]http://kaldi-asr.org/doc/data_prep.html
export LC_ALL=C 

possible problem:
the speaker-id should be a prefix of the utterance-id  
[source](https://sourceforge.net/p/kaldi/discussion/1355347/thread/1012cc7b/)
