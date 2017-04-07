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
in `run.sh`, a shell script called `data_prep.sh` will be execuated to prepare audio and acoustic data, along with fixing and validating the directories. 

### local
contains data preperation script and its README file   
within `data_prep.sh`, it calls `audio_data_prep.py` and `acoustic_data_prep.py` to prepare audio and acoustic data, along with native Kaldi script to generate `spk2utt`, sorting files and validate `data/train` and `data/test` directories. 


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
### 6. Install srilm to build the ARPA language model 

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

### 7. create G.fst using the ARPA language model
```
 lang=data/lang
 local=data/local
 arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst
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
