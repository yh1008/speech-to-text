
## GMM ReAlignment
### Example in Kaldi: [hkust](https://github.com/kaldi-asr/kaldi/tree/master/egs/hkust/s5)
- Steps
  - monophone
  - tri1 on monophone [first triphone pass]
  - tri2 on tri1 [delta+delta-deltas]
  - tri3a on tri2 [LDA+MLLT]
  - tri4a on tri3a [fmllr]
  - tri5a on tri4a [SAT]
```
# for x in exp/*/decode; do [ -d $x ] && grep WER $x/cer_* | utils/best_wer.sh; done
%WER 80.72 [ 45327 / 56154, 1609 ins, 10856 del, 32862 sub ] exp/mono0a/decode/cer_9
%WER 58.86 [ 33054 / 56154, 2651 ins, 6240 del, 24163 sub ] exp/tri1/decode/cer_13
%WER 58.32 [ 32748 / 56154, 2491 ins, 6279 del, 23978 sub ] exp/tri2/decode/cer_14
%WER 56.49 [ 31719 / 56154, 2601 ins, 5979 del, 23139 sub ] exp/tri3a/decode/cer_13
%WER 51.75 [ 29060 / 56154, 2879 ins, 5088 del, 21093 sub ] exp/tri4a/decode/cer_13
%WER 47.36 [ 26596 / 56154, 2740 ins, 4577 del, 19279 sub ] exp/tri5a/decode/cer_13
%WER 42.55 [ 23894 / 56154, 1877 ins, 4437 del, 17580 sub ] exp/tri5a_mpe/decode/cer_13
%WER 42.19 [ 23693 / 56154, 2138 ins, 3871 del, 17684 sub ] exp/tri5a_mmi_b0.1/decode/cer_10
%WER 41.11 [ 23086 / 56154, 2863 ins, 3608 del, 16615 sub ] exp/sgmm2_5a/decode/cer_10

# nnet2 online results
%WER 38.32 [ 21518 / 56154, 2344 ins, 4273 del, 14901 sub ] exp/nnet2_online/nnet_ms/decode/cer_12
%WER 38.01 [ 21345 / 56154, 2555 ins, 4173 del, 14617 sub ] exp/nnet2_online/nnet_ms_online/decode/cer_12
%WER 37.10 [ 20832 / 56154, 2399 ins, 3936 del, 14497 sub ] exp/nnet2_online/nnet_ms_online/decode_per_utt/cer_12

# nnet3 online results
%WER 32.77 [ 18400 / 56154, 1971 ins, 3525 del, 12904 sub ] exp/nnet3/tdnn_sp/decode/cer_10
%WER 33.02 [ 18540 / 56154, 2335 ins, 3251 del, 12954 sub ] exp/nnet3/tdnn_sp_online/decode/cer_9
%WER 34.01 [ 19098 / 56154, 2195 ins, 3482 del, 13421 sub ] exp/nnet3/tdnn_sp_online/decode_per_utt/cer_10

# chain online results
%WER 28.24 [ 15858 / 56154, 1454 ins, 3415 del, 10989 sub ] exp/chain/tdnn_7h_sp/decode/cer_10
%WER 28.16 [ 15812 / 56154, 1648 ins, 2824 del, 11340 sub ] exp/chain/tdnn_7h_sp_online/decode/cer_9
%WER 29.55 [ 16594 / 56154, 1547 ins, 3437 del, 11610 sub ] exp/chain/tdnn_7h_sp_online/decode_per_utt/cer_10
```




## Speech Data Augmentation
### Related Paper
- [Audio Augmentation for Speech Recognition](http://www.danielpovey.com/files/2015_interspeech_augmentation.pdf)
>In this paper, we investigate audio-level speech augmentation methods which directly process the raw signal. The method we particularly recommend is to change the speed of the audio signal, producing 3 versions of the original signal with speed factors of 0.9, 1.0 and 1.1. The proposed technique has a low implementation cost, making it easy to adopt. We present results on 4 different LVCSR tasks with training data ranging from 100 hours to 1000 hours, to examine the effectiveness of audio augmentation in a variety of data scenarios. An average relative improvement of 4.3% was observed across the 4 tasks.
- [Vocal Tract Length Perturbation (VTLP) improves speech recognition](http://www.cs.toronto.edu/~ndjaitly/jaitly-icml13.pdf)
> At test time, a prediction is made by averaging the predictions over multiple warp factors. When this technique is applied to TIMIT using Deep Neural Networks (DNN) of different depths, the Phone Error Rate (PER) improved by an average of 0.65% on the test set. For a Convolutional neural network (CNN) with convolutional layer in the bottom, a gain of 1.0% was observed. These improvements were achieved without increasing the number of training epochs, and suggest that data transformations should be an important component of training neural networks for speech, especially for data limited projects.

### Speed perturbation in Kaldi: [run_ivector_common.sh](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/local/nnet3/run_ivector_common.sh)
### Reverberate in Kaldi: [reverberate_data_dir.py](https://github.com/kaldi-asr/kaldi/blob/master/egs/wsj/s5/steps/data/reverberate_data_dir.py)
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
