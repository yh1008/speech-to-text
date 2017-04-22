## Speech Data Augmentation
### Kaldi: [reverberate_data_dir.py](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/steps/data/reverberate_data_dir.py)
- path: kaldi/egs/wsj/s5/steps/data/reverberate_data_dir.py
- usage: reverberate_data_dir.py [options...] <in-data-dir> <out-data-dir>
- example
```
reverberate_data_dir.py --rir-set-parameters rir_list --foreground-snrs 20:10:15:5:0 \
--background-snrs 20:10:15:5:0 --noise-list-file noise_list --speech-rvb-probability 1 \
--num-replications 2 --random-seed 1 data/train data/train_rvb
```
- options description

|  option |  usage  |  input  |
|---------|-----|-------------|
|--rir-set-parameters|Specifies the parameters of an RIR set. <br>Supports the specification of mixture_weight and rir_list_file_name. The mixture weight is optional. The default mixture weight is the probability mass remaining after adding the mixture weights of all the RIR lists, uniformly divided among the RIR lists without mixture weights.|the format of the RIR list file is: <br> --rir-id <string,required> --room-id <string,required> --receiver-position-id <string,optional> --source-position-id <string,optional> --rt-60 <float,optional> --drr <float, optional> location <rspecifier>|
|--noise-set-parameters|Specifies the parameters of an noise set. <br>Supports the specification of mixture_weight and noise_list_file_name. The mixture weight is optional. The default mixture weight is the probability mass remaining after adding the mixture weights of all the noise lists, uniformly divided among the noise lists without mixture weights.|the format of the noise list file is<br>--noise-id <string,required> --noise-type <choices = {isotropic, point source},required> --bg-fg-type <choices = {background, foreground}, default=background> --room-linkage <str, specifies the room associated with the noise file. Required if isotropic> location <rspecifier>|--noise-id 001 --noise-type isotropic --rir-id 00019 iso_noise.wav|

- options guide

|  option | required|default| usage example | input example  |
|---------|-----|---|----|------|
|--rir-set-parameters|Y| |--rir-set-parameters '0.3, rir_list' or 'rir_list'| --rir-id 00001 --room-id 001 --receiver-position-id 001 --source-position-id 00001 --rt60 0.58 --drr -4.885 data/impulses/Room001-00001.wav|
|--noise-set-parameters| |None|--noise-set-parameters '0.3, noise_list' or 'noise_list'|--noise-id 001 --noise-type isotropic --rir-id 00019 iso_noise.wav|


## RNN LM Rescoring
### Kaldi: [rnnlmrescore.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/steps/rnnlmrescore.sh)
