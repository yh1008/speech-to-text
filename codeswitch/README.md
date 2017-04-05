# codeswitch directory description

move this `codeswitch` directory under `kaldi/egs/`
```
cp codeswitch ./kaldi/egs/
```
also put the `LDC2015S04` raw data folder under `kaldi/egs/codeswitch` 


### run.sh
contains the script to prepare acoustic data and create MFCC feature extractions, (soon to be language model generation, tri-phone alignment, DNN and decode)
to execute:
```
./run.sh
```

### local
contains data preperation script and its README file   
to execute:
```
chmod 755 local/audio_data_prep.py
chmod 755 local/acoustic_data_prep.py

./local/audio_data_prep.py
./local/acoustic_data_prep.py
```


### path.sh 
tells where to find kaldi binary `. ./path.sh` is executed on all shell script to set the kaldi environment variable. 
to manually check if it is setted, use command
```
echo $KALDI_ROOT
```


## Language Model Preparation
### 1. Combine and fix the transcripts
#### Folder: data/train, data/test
#### File created: text
#### File content: all the sentences in transcripts, with utterance id and sentence transcript
Transcripts under folder data/train and data/test should be like the following, where a **unique utterance id** (if a speaker has more than one utterance, the utterance id is not the speaker id) is followed by a sentence.
```
110236_20091006_82330_F_0001 I'M WORRIED ABOUT THAT
110236_20091006_82330_F_0002 AT LEAST NOW WE HAVE THE BENEFIT
110236_20091006_82330_F_0003 DID YOU EVER GO ON STRIKE
...
120958_20100126_97016_M_0285 SOMETIMES LESS IS BETTER
120958_20100126_97016_M_0286 YOU MUST LOVE TO COOK
```

Our data has multiple utterances for a speaker, so we need to
- match utterance id and speaker id by creating a segment file like this, with utterance id, speaker id, start time, end time:
```
110236_20091006_82330_F_001 110236_20091006_82330_F 0.0 3.44
110236_20091006_82330_F_002 110236_20091006_82330_F 4.60 8.54
...
120958_20100126_97016_M_285 120958_20100126_97016_M 925.35 927.88
120958_20100126_97016_M_286 120958_20100126_97016_M 928.31 930.51
```
- remove the start time and end time in the original transcript and replace the unique speaker id with the unique utterance id
- combine all the sentences in training data as a whole (and the same to test data)

### 2. Get word list
#### Folder: data/train, data/test
#### File created: words.txt
#### File content: all the unique words in text
```
cut -d ' ' -f 2- text | sed 's/ /\n/g' | sort -u > words.txt
```

### 3. Filter lexicon
#### Folder: data/local/lang
#### File created: lexicon.txt
#### File content: the pronunciation (phones) of words that appear in the data
Using python script

### 4. Create phone list
#### Folder: data/local/lang
#### File created: nonsilence_phone.txt, silence_phone.txt, optional_silence.txt
#### File content: the range of phones
silence_phone.txt is from python script
```
cut -d ' ' -f 2- lexicon.txt | sed 's/ /\n/g' | sort -u > nonsilence_phones.txt
echo 'SIL' > optional_silence.txt
```

### 5. Generate other files
#### Folder: codeswitch
#### File created: phones (folder), oov.txt, L.fst
#### File content: 
```
cd codeswitch
utils/prepare_lang.sh data/local/lang '<oov>' data/local/ data/lang
```

## Decoding Phase
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
