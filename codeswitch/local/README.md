# Local Directory Description
### Table of Content 
- [data_prep.sh](#dp)
  - [acoustic_data_prep.py](#adp)
  - [audio_data_prep.py](#audiodp)
  - [lang_data_perp.py](#ldp)
- [MER Scoring](#mer)
- [online Directory Description](#online)
- [ext Directory Description](#ext)
- [asset Directory Description(#assets)

### <a name="dp"></a>data_prep.sh
the essential script to prepare audio, acoustic, language data, and install neccessarily toolkit to build language models  

#### <a name="adp"></a>acoustic_data_prep.py
author: Emily Hua  
prepares spk2gender, utt2spk, segments, text, wav.scp for data/train and data/test 

#### <a name="audiodp"></a>audio_data_prep.py
author: Emily Hua  
prepares audio directory for Kaldi to consume 

#### <a name="ldp"></a>lang_data_prep.py
author: Wendy Wang  
prepares lexicon, silence_phones.txt

### <a name="mer"></a>MER scoring 
author: SpacePineapple, Emily Hua  
calculate M(ix) E(rror) R(ate), Insertion, Substituion and Deletion Error for English and Chinese seperately (on either word or character level) 

### <a name="online"></a> Online   
contains the neural network code modified for this task. [taken from egs/wsj/s5/local/online](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/local/online/run_nnet2_baseline.sh)

### <a name="ext"></a> Ext   
contains perl and shell script to calculate Chinese C(harecter)E(rror)R(ate). [taken from egs/hkust/s5/local/ext](https://github.com/kaldi-asr/kaldi/tree/master/egs/hkust/s5/local/ext)

### <a name="assets"></a> Asset
contains intermediate jupyter notebooks 

