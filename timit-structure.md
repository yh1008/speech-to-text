# TIMIT Study

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
