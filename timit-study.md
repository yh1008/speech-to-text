# TIMIT Study

### specs
8 core Ubuntu 16.04 LTS Google Cloud VM    
finish ./run.sh in 3 hours  
finish ./run_kt.sh in 2.5 hours

### pre-run.sh: file structure of kaldi/egs/timit/s5/
```
yh2901@instance-1:~/kaldi/egs/timit/s5$ tree .
.
├── cmd.sh
├── conf
│   ├── dev_spk.list
│   ├── fbank.conf
│   ├── mfcc.conf
│   ├── phones.60-48-39.map
│   └── test_spk.list
├── local
│   ├── nnet
│   │   ├── run_autoencoder.sh
│   │   └── run_dnn.sh
│   ├── score_basic.sh
│   ├── score_combine.sh
│   ├── score_sclite.sh
│   ├── score.sh -> score_sclite.sh
│   ├── timit_data_prep.sh
│   ├── timit_format_data.sh
│   ├── timit_norm_trans.pl
│   └── timit_prepare_dict.sh
├── path.sh
├── RESULTS
├── run.sh
├── steps -> ../../wsj/s5/steps
├── timit.zip
└── utils -> ../../wsj/s5/utils
```

### modification to run on CPU 
1. to avoid qsub not found error
```steps/make_mfcc.sh --cmd queue.pl -l arch=*64 --nj 30 data/train exp/make_mfcc/train mfcc
steps/make_mfcc.sh: [info]: no segments file exists: assuming wav.scp indexed by utterance.
queue.pl: error submitting jobs to queue (return status was 32512)
sh: 1: qsub: not found
```
in cmd.sh 
change 
```
export train_cmd="queue.pl --mem 4G"
export decode_cmd="queue.pl --mem 4G"
export mkgraph_cmd="queue.pl --mem 8G"
# the use of cuda_cmd is deprecated but it's still sometimes used in nnet1
# example scripts.
export cuda_cmd="queue.pl --gpu 1"
```
to 
```
export train_cmd="run.pl"
export decode_cmd="run.pl"
export mkgraph_cmd="run.pl"
export cuda_cmd="run.pl"
```
- [reference](https://sourceforge.net/p/kaldi/discussion/1355348/thread/98345f33/)  

2. to avoid bc: command not found error 
```
local/score.sh: line 56: bc: command not found
run.pl: 5 / 5 failed, log is in exp/mono/decode_dev/scoring/log/best_path.1.*.log
steps/decode.sh: Scoring failed. (ignore by '--skip-scoring true')
```
do 
```
$sudo apt-get install bc
```

### best kaldi tutorial 
- [University of Edinburgh-Automatic Speech Reconigtion course](https://www.inf.ed.ac.uk/teaching/courses/asr/2016-17/lab1.pdf)
made in 2017  
contains:  
1. Kaldi recipe file structure explanations:   
   **path.sh** contains environment variable KALDI_ROOT to point to the Kaldi installation.     
   **exp** contains the actual experiments, models and their logs.     
   **local** contains files that relate only to the corpus we are working on.    
   to check that the data directories conforms to Kaldi specifications, run the next two lines in **run.sh**:  
   ```
   utils/validate_Data_dir.sh data/train
   utils/validate_data_dir.sh data/test
   ```
   
      
2. MFCC feature extractions:      
   scripts and archives:     
   
   *.scp files map utterance if to position in *.ark files. The latter contains the actual data.    
   
   **scp:feats.scp** to read   
   
   **ark:mfcc.ark** to write to stdout. Archives will be written in binary; to avoid it append the **,t** modifier  **ark,t:mfcc.ark**
