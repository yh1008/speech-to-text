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
|--num-replications |Number of replicate to generated for the data |  |
|--foreground-snrs |When foreground noises are being added the script will iterate through these SNRs. |  |
|--background-snrs |When background noises are being added the script will iterate through these SNRs. |  |
|--prefix |This prefix will modified for each reverberated copy, by adding additional affixes. |  |
|--speech-rvb-probability|Probability of reverberating a speech signal, e.g. 0 <= p <= 1| |
|--pointsource-noise-addition-probability|Probability of adding point-source noises, e.g. 0 <= p <= 1| |
|--isotropic-noise-addition-probability|Probability of adding isotropic noises, e.g. 0 <= p <= 1| |
|--rir-smoothing-weight|Smoothing weight for the RIR probabilties, e.g. 0 <= p <= 1. If p = 0, no smoothing will be done. <br>The RIR distribution will be mixed with a uniform distribution according to the smoothing weight.| |
|--noise-smoothing-weight|Smoothing weight for the noise probabilties, e.g. 0 <= p <= 1. If p = 0, no smoothing will be done.<br>The noise distribution will be mixed with a uniform distribution according to the smoothing weight.| |
|--max-noises-per-minute|This controls the maximum number of point-source noises that could be added to a recording according to its duration.| |
|--random-seed|seed to be used in the randomization of impulses and noises| |
|--shift-output|If true, the reverberated waveform will be shifted by the amount of the peak position of the RIR| |
|--source-sampling-rate|Sampling rate of the source data. If a positive integer is specified with this option, the RIRs/noises will be resampled to the rate of the source data.| |
|--include-original-data|If true, the output data includes one copy of the original data| |
|input_dir|Input data directory| |
|output_dir|Output data directory| |

- options guide

|  option | required|default| usage example | input example  |
|---------|-----|---|----|------|
|--rir-set-parameters|Y| |--rir-set-parameters '0.3, rir_list' or 'rir_list'| --rir-id 00001 --room-id 001 --receiver-position-id 001 --source-position-id 00001 --rt60 0.58 --drr -4.885 data/impulses/Room001-00001.wav|
|--noise-set-parameters| |None|--noise-set-parameters '0.3, noise_list' or 'noise_list'|--noise-id 001 --noise-type isotropic --rir-id 00019 iso_noise.wav|
|--num-replications| |1| | |
|--foreground-snrs| |20:10:0| | |
|--background-snrs| |20:10:0| | |
|--prefix| |None| | |
|--speech-rvb-probability| |1.0| | |
|--pointsource-noise-addition-probability| |1.0| | |
|--isotropic-noise-addition-probability| |1.0| | |
|--rir-smoothing-weight| |0.3| | |
|--noise-smoothing-weight| |0.3| | |
|--max-noises-per-minute| |2| | |
|--random-seed| |0| | |
|--shift-output| |true| | |
|--source-sampling-rate| |None| | |
|--include-original-data| |false| | |


## RNN LM Rescoring
### Kaldi: [rnnlmrescore.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/steps/rnnlmrescore.sh)

## Tandem system with deep bottleneck features
### Kaldi+PDNN: [shell scripts & benchmark results](https://www.cs.cmu.edu/~ymiao/kaldipdnn.html)
