# Mixlingual Speech-To-Text project

### From the team:   
As Chinese students studying in the states, we found our speaking habits morphed -- English words and phrases easily get slipped into Chinese sentences. We greatly feel the need to have messaging apps that can handle multilingual speech-to-text translation. So in this task, we are going to develop this function -- build a model using deep learning technologies to corretly translate multilingual audio (having Chinese and English in the same sentence) into text.

### Data Source:
- [Mandarin-English Code-Switching in South-East Asia](https://catalog.ldc.upenn.edu/ldc2015s04)   

### Baseline Model Paper:
- [A Chinese-English Mixlingual Database and A Speech Recognition Baseline](https://arxiv.org/pdf/1609.08412v1.pdf)

### Other Code-switching related Paper:
- [A First Speech Recognition System For Mandarin-English Code-switch Conversational Speech](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6289015)
- [Speech Recognition on English-Mandarin Code-Switching Data using Factored Language Models](http://www.csl.uni-bremen.de/cms/images/documents/publications/DA_JanGebhardt.pdf)

### Feature Improvement related Paper:
- [Improved feature processing for Deep Neural Networks](http://www.danielpovey.com/files/2013_interspeech_nnet_lda.pdf)  
- [iVector](http://people.csail.mit.edu/sshum/talks/ivector_tutorial_interspeech_27Aug2011.pdf)

### Interesting Python Kaldi Wrapper to be examined:
- [Pykaldi](https://github.com/UFAL-DSG/pykaldi/tree/master/pykaldi) 
- [Alex Dialog System Framwork](http://alex.readthedocs.io/en/master/_man_rst/alex.tools.kaldi.README.html)  

### Kaldi recommended recipe to be examined:
- [Librispeech](http://www.openslr.org/11/)    

### Kaldi resources:
- [Daniel Povey Lectures](http://www.danielpovey.com/kaldi-lectures.html)
- [An Introduction to Kaldi Toolkit](http://berlin.csie.ntnu.edu.tw/Courses/Speech%20Recognition/Lectures2013/SP2013F_Lecture14-Introduction%20to%20the%20Kaldi%20toolkit.pdf)
- [Building Speech Recognition Systems with the Kaldi Toolkit](https://engineering.jhu.edu/clsp/wp-content/uploads/sites/75/2016/06/Building-Speech-Recognition-Systems-with-the-Kaldi-Toolkit.pdf)
- [Kaldi Document in CN](https://shiweipku.gitbooks.io/chinese-doc-of-kaldi/content/index.html)
- [University of Edinburgh-Automatic Speech Reconigtion Course Lab](https://www.inf.ed.ac.uk/teaching/courses/asr/2016-17/lab1.pdf)
- [Kaldi Data Prep (Eleanor Chodroff)](http://pages.jh.edu/~echodro1/tutorial/kaldi/kaldi-training2.html)
- [Kaldi Data Prep (kaldi-asr.org)](http://kaldi-asr.org/doc/data_prep.html)
- Kaldi excamples
  - [Resource Management](http://kaldi-asr.org/doc/tutorial_running.html)
  - [Speech-to-Text in Swedish using Kaldi](http://www.diva-portal.org/smash/get/diva2:949757/FULLTEXT01.pdf)
- Decoding
  - [Online decoding in Kaldi](http://kaldi-asr.org/doc/online_decoding.html) 
  - [Decoding Lecture slides](http://danielpovey.com/files/Lecture4.pdf)
  - [Kaldi decoder document](http://www.hark.jp/document/2.3.0/hark-document-en/subsec-KaldiDecoder.html)
  - [How to use an Existing DNN Recognizer for Decoding in Kaldi](http://jrmeyer.github.io/kaldi/2017/01/10/Using-built-DNN-model-Kaldi.html)
  - [Understanding the decoding graph construciton](http://vpanayotov.blogspot.com/2012/06/kaldi-decoding-graph-construction.html)


### Data Preperation:
- [Kaldi for Dummies Tutorial](http://kaldi-asr.org/doc/kaldi_for_dummies.html  )  
  
|  | filename: |  pattern: | format: |path: | source:|
| ------------- | ------------- |-|-|--|--|
|acoustic data:   |spk2gender  |\<speakerID>\<gender> | |/data/train /data/test | handmade|
|  | utt2spk    |\<utteranceID>\<speakerID> | | /data/train /data/test| handmade | 
|  | wav.scp    |\<utteranceID>\<full_path_to_audio_file>| .scp: kaldi script file|/data/train /data/test | handmade|
|  | text       |\<utteranceID>\<full_path_to_audio_file> |.ark: kaldi archive file| /data/train /data/test|  exists | 
|language data:  | lexicon.txt |\<word> \<phone 1>\<phone 2> ... | .ark: kaldi archive file |data/local/dict| egs/voxforge|
|  | nonsilence_phones.txt | \<phone>| |data/local/dict | unkown | 
|  |silence_phones.txt   |\<phone> | |data/local/dict |unkown |
|  | optional_silence.txt |\<phone> |  | data/local/dict| unkown | 
|Tools:  | utils | | | / | kaldi/egs/wsj/s5|   
|  |steps  | | | / | kaldi/egs/wsj/s5 |
|  | score.sh | | | /| kaldi/egs/voxforge/s5/local |   

### Language Model:
- [ARPA LM format](http://www1.icsi.berkeley.edu/Speech/docs/HTKBook3.2/node213_mn.html)   

What are our language model:  
3-grams trained from the transcripts of THCHS30 + LDC2015S04    

directory structure taken from /egs/TIMIT/s5: 
```
/data
  /local
    /nist_lm
      /lm_phone_bg.arpa.gz
```  
How to build a language model: 
- [SRILM](http://www.speech.sri.com/projects/srilm/)
- [Kaldi lm_build ](https://github.com/srvk/lm_build)
- [egs/babel/s5/local/train_lms_srilm.sh built using SRILM toolkit](https://github.com/kaldi-asr/kaldi/blob/master/egs/babel/s5/local/train_lms_srilm.sh) 
- [Language Preparation](http://white.ucc.asn.au/Kaldi-Notes/tidigits/lang_prep)

Kaldi script utils/prepare_lang.sh
```
usage: utils/prepare_lang.sh <dict-src-dir> <oov-dict-entry> <tmp-dir> <lang-dir>
e.g.: utils/prepare_lang.sh data/local/dict <SPOKEN_NOISE> data/local/lang data/lang
options:
     --num-sil-states <number of states>             # default: 5, #states in silence models.
     --num-nonsil-states <number of states>          # default: 3, #states in non-silence models.
     --position-dependent-phones (true|false)        # default: true; if true, use _B, _E, _S & _I
                                                     # markers on phones to indicate word-internal positions.
     --share-silence-phones (true|false)             # default: false; if true, share pdfs of
                                                     # all non-silence phones.
     --sil-prob <probability of silence>             # default: 0.5 [must have 0 < silprob < 1]
```
Turning the –share-silence-phones option to TRUE was extremely helpful for the Cantonese data of IARPA's BABEL project, where the data is very messy and has long untranscribed portions that the Kaldi developers try to align to a special phone that is designated for that purpose.
The --sil-prob might be another potentially important option.

#### Preparation
- lexicon.txt
  - The pronunciation dictionary where every line is a word with its phonemic pronunciation. It Only contains words and their pronunciations that are present in the corpus.
  - ENG: [CMU dictionary](http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/)
- nonsilence_phones.txt
- optional_silence.txt
- silence_phones.txt 

### MFCC Feature Extraction: 
```
   echo
   echo "===== FEATURES EXTRACTION ====="
   echo
 
   # Making feats.scp files
   mfccdir=mfcc
   # Uncomment and modify arguments in scripts below if you have any problems with data sorting
   # utils/validate_data_dir.sh data/train     # script for checking prepared data - here: for data/train directory
   # utils/fix_data_dir.sh data/train          # tool for data proper sorting if needed - here: for data/train directory
   steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/train exp/make_mfcc/train $mfccdir
   steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/test exp/make_mfcc/test $mfccdir
  
   # Making cmvn.scp files
   steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfccdir
   steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir
```
MFCC-related documents
- [MFCC extraction in detail (CN)](https://my.oschina.net/jamesju/blog/193343)

### HMM - GMM 
[Reference](http://www.inf.ed.ac.uk/teaching/courses/asr/2012-13/asr03-hmmgmm-4up.pdf)  

![a](https://latex.codecogs.com/gif.latex?a_%7Bij%7D) as the transition probability from state i to state j   
![b](https://latex.codecogs.com/gif.latex?b_j%28X%29) as the emission probability from state j to sequence X  

Forward-backward algorithm fine tunes ![a](https://latex.codecogs.com/gif.latex?a_%7Bij%7D)  

GMM provides![b](https://latex.codecogs.com/gif.latex?b_j%28X%29)  

HMM solves the following three problems:  
1. overall likelihood (Forward algorithm): determine the likelihood of an observation sequence X=(x1, x2, ... xT) being generated by an HMM 
2. training (Forward-backward algorithm EM): given an observation sequence, learn the best ![lambda](https://latex.codecogs.com/gif.latex?%5Clambda%5C%7B%20a_%7Bij%7D%2C%20b_j%28X%29%20%5C%7D)
3. decoding (Viterbi algorithm): given an on observation sequence, determine the most probable hidden state sequence

### CNN and MFSC features

In order to train CNN, we need to extract MFSC features from the acoustic data instead of MFCC features, as Discrete Cosine Transformation (DCT) in MFCC destroys locality. MFSC features also called filter banks. In Kaldi, the scripts are something like the following: 
```
steps/make_fbank.sh --nj 3 \ $trainDir/train_clean_fbank exp/make_fbank/train_clean_fbank feat/fbank/ || exit 1;
steps/compute_cmvn_stats.sh $trainDir/train_clean_fbank exp/make_fbank/train_clean_fbank feat/fbank/ || exit 1;
```
notice that fbanks don't work well with GMM as fbanks features are highly correlated, and GMM modelled with diagonal covariance matrices assumed independence of feature streams. fbanks/MFSC is okay with DNN, best for CNN.   
[why MFSC+GMM produced high WER-see Kaldi discussion](https://sourceforge.net/p/kaldi/discussion/1355348/thread/ddf22517/?limit=25)   
[why DCT destroys locality-see post](http://dsp.stackexchange.com/questions/31917/why-discrete-cosine-transform-may-not-maintain-locality)

### Run Kaldi on single GPU

This doesn't require Sun GridEngine. 
Simply download [CUDA toolkit] (https://developer.nvidia.com/cuda-downloads), install it with
```
sudo sh cuda_8.0.61_375.26_linux.run
```
and then go under kaldi/src execute
```
./configure
```
to check if it detects CUDA, you will also find `CUDA = true` in kaldi/src/kaldi.mk
then recompile Kaldi with
```
make -j 8 # 8 for 8-core cpu
make depend -j 8 # 8 for 8-core cpu
```

Noted that GMM-based training and decode is not supported by GPU, only `nnet` does. [source](https://groups.google.com/forum/#!topic/kaldi-help/bLd2TvT4cDE)

**
if you are using AWS g2.2xlarge, and launched the instance before 2017-04-18 (when this note is written), its NVIDIA may need a legacy 367.x driver, the default (latest) driver that comes with CUDA-8 `cuda_8.0.61_375.26_linux.run` will fail. 
To check the current version of the driver installed on the instance, type
```
apt-cache search nvidia | grep -P '^nvidia-[0-9]+\s'
```
to install a version of your choice from the list, type
```
sudo apt-get install nvidia-367
```
You can also download a specifc version from the web, for example [`NVIDIA-Linux-x86_64-367.18.run`](http://www.nvidia.com/Download/driverResults.aspx/102879/en-us). Install it with 
```
sudo sh NVIDIA-Linux-x86_64-367.18.run
```
and then when installing `cuda_8.0.61_375.26_linux.run`, it will ask you whether to install NVIDIA driver 375, make sure you choose `no`. 

### Install tensorflow-gpu 
Required:
1. [install CUDA toolkit](https://developer.nvidia.com/cuda-downloads) 8.0 as of 04-18-2017   
2. [install cuDNN](https://developer.nvidia.com/cudnn) download v5, as of 04-18-2017, Tensorflow performs the best with cuDNN 5.x     
Follow commands carefully from the [Tensorflow website](https://www.tensorflow.org/versions/r0.11/get_started/os_setup#optional_install_cuda_gpus_on_linux).
After intallation, you can test if tensorflow can detect your gpu by typing the following: 
```
# makes sure you are out of the tensorflow git repo
python
>>> import tensorflow as tf
>>> sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
```
A working tensorflow will output:
```
I tensorflow/core/common_runtime/gpu/gpu_device.cc:885] Found device 0 with properties: 
name: Tesla K80
major: 3 minor: 7 memoryClockRate (GHz) 0.8235
pciBusID 0000:00:04.0
Total memory: 11.17GiB
Free memory: 11.11GiB
I tensorflow/core/common_runtime/gpu/gpu_device.cc:906] DMA: 0 
I tensorflow/core/common_runtime/gpu/gpu_device.cc:916] 0:   Y 
I tensorflow/core/common_runtime/gpu/gpu_device.cc:975] Creating TensorFlow device (/gpu:0) -> (device: 0, name: Tesla K80, pci bus id: 0000:00:04.0)
Device mapping:
/job:localhost/replica:0/task:0/gpu:0 -> device: 0, name: Tesla K80, pci bus id: 0000:00:04.0
I tensorflow/core/common_runtime/direct_session.cc:257] Device mapping:
/job:localhost/replica:0/task:0/gpu:0 -> device: 0, name: Tesla K80, pci bus id: 0000:00:04.0

```
1. During testing, if you run into error like:
```
I tensorflow/stream_executor/dso_loader.cc:126] Couldn't open CUDA library libcudnn.so.5. LD_LIBRARY_PATH: /usr/local/cuda/lib64
I tensorflow/stream_executor/cuda/cuda_dnn.cc:3517] Unable to load cuDNN DSO
```
from the writer's experience, you didn't set the right `LD_LIBRARY_PATH` in the `~/.profile` file. You need to examine where is `libcudnn.so.5` located and move it to the desired location, most likely it will be `/usr/local/cuda`. Also make sure you type `source ~/.profile` to activate the change, after you modify the file.    

2. If you are testing it in a python shell, and you met the following error:
```
ImportError: libcudart.so.8.0: cannot open shared object file: No such file or directory
```
very likely you are in the actual `tensorflow` git repo. [source](https://github.com/tensorflow/tensorflow/issues/8107), make sure you jump out of it before testing. 


### Kaldi script to train nnet

1. 3-4 hours to train, 3 hours to decode on GPU:   
[local/online/run_nnet2_baseline.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/local/online/run_nnet2.sh)

### Chinese CER (Character Error Rate)

1. [egs/hkust/s5/local/ext/score.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/hkust/s5/local/ext/score.sh)
