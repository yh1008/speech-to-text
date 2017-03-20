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

### three-state HMM topology  
stored in data/lang/topo
```
less data/lang/topo
```
```
<Topology>
<TopologyEntry>
<ForPhones>
2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 3
2 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48
</ForPhones>
<State> 0 <PdfClass> 0 <Transition> 0 0.75 <Transition> 1 0.25 </State>
<State> 1 <PdfClass> 1 <Transition> 1 0.75 <Transition> 2 0.25 </State>
<State> 2 <PdfClass> 2 <Transition> 2 0.75 <Transition> 3 0.25 </State>
<State> 3 </State>
</TopologyEntry>
<TopologyEntry>
<ForPhones>
1
</ForPhones>
<State> 0 <PdfClass> 0 <Transition> 0 0.5 <Transition> 1 0.5 </State>
<State> 1 <PdfClass> 1 <Transition> 1 0.5 <Transition> 2 0.5 </State>
<State> 2 <PdfClass> 2 <Transition> 2 0.75 <Transition> 3 0.25 </State>
<State> 3 </State>
</TopologyEntry>
</Topology>
```
We can see that phone 1 has different toppology than the rest 2-48.  
The transition probabilities are defined after the \<Transition> tags.

### Inspect Monophone Model 
```
gmm-copy --binary=false exp/mono/0,mdl - | less
```
Model file contains transition-model object, then GMM object [p35](http://www.danielpovey.com/files/Lecture2.pdf)  
We first see something similar to the above 3-state HMM topology. Followed by \<Triples> tags, which map each phone and one of its three states to a unique number. Pattern: \<phone number> \<state number> \<unique number>.   

```
</DiagGMM> 
<DiagGMM> 
<GCONSTS>  [ -92.5587 ]
<WEIGHTS>  [ 1 ]
<MEANS_INVVARS>  [
  0.0001885423 -9.16086e-05 -0.002972129 3.875432e-05 -0.001368281 0.001315587 -0.002500096 0.002315077 0.00429833 -0.001668188 -0.000945402 -0.004315328 0.003369074 -0.0009874019 -0.0005568534 0.0007905881 -0.0008598298 0.0001569456 0.001501414 9.160395e-06 -0.0001019144 -0.0002464386 0.0002609729 0.001031367 -0.001062488 -0.002340279 0.0008570973 0.0003101975 -0.0005292972 0.001775443 0.0002102287 8.378625e-05 -1.217527e-06 -0.0002182741 -0.0002974362 -0.0009353954 0.0004943676 0.001565399 0.001386349 ]
<INV_VARS>  [
  0.005339943 0.002408599 0.005009499 0.004234992 0.003415213 0.004226068 0.003845918 0.004330037 0.004469929 0.00555164 0.006493011 0.007199864 0.01219888 0.0938514 0.05168371 0.07636816 0.08218509 0.06499127 0.06110011 0.06516927 0.05807921 0.06776563 0.07036626 0.08379282 0.1019901 0.1359497 0.5388283 0.371821 0.4569601 0.5199628 0.4027453 0.3459871 0.3799254 0.3325204 0.3964455 0.3940115 0.4471866 0.5627591 0.7084802 ]
</DiagGMM> 
```
Here DiagGMM stores parameters of each single diagonal-covariance Gaussian Mixture Model as: inverse variances, and (means times inverse variances)  [source](http://kaldi-asr.org/doc/model.html)  

There will be many monophone models created, the final model summary information can be found using:
```
gmm-info exp/mono/final.mdl
```

to look at the alignment of the monophone model:  
```
copy-int-vector "ark:gunzip -c exp/mono/ali.1.gz|" ark,t:- | head -n 1
```  
alignments are in gzip format. The above command unzip the file and pipe them directly in as the read specifier. Then apply **ark,t:-** to get readable output from the write specifier. **head -n 1** only shows the first line.    
we get the following output:
```
faem0_si1392 2 4 3 3 3 3 3 3 6 5 5 5 5 38 37 37 37 40 42 218 217 217 217 217 217 21
7 217 217 217 217 217 217 220 219 222 221 248 247 247 247 247 247 247 250 252 176 1
75 178 177 177 177 177 177 180 122 121 121 121 121 121 121 121 124 123 126 125 125 
26 28 27 30 29 29 212 211 214 216 215 146 148 150 260 262 261 264 263 278 277 277 2
77 280 282 281 281 14 13 13 13 13 13 16 15 18 17 17 176 178 180 62 64 66 206 208 21
0 242 241 244 246 170 169 169 169 169 172 171 171 174 173 173 173 173 38 37 37 37 4
0 42 41 218 217 217 217 217 217 217 217 217 217 220 219 222 146 145 148 147 150 62 
64 66 56 55 55 55 55 55 58 57 60 59 59 248 250 249 249 252 251 251 251 251 251 116 
115 115 115 118 117 117 120 119 224 223 223 223 223 223 223 226 225 225 228 98 97 9
7 100 99 102 101 266 265 265 265 265 268 267 267 267 270 269 269 86 88 90 110 112 1
11 111 114 122 121 121 121 121 121 121 121 121 121 124 123 126 125 125 8 7 7 7 7 7 
7 7 10 9 9 12 212 214 216 176 175 175 178 177 180 134 133 133 133 136 135 138 137 8
6 88 87 90 278 277 277 277 280 279 282 281 38 37 40 42 62 64 66 206 205 208 207 207
 207 207 207 210 209 14 13 16 15 15 15 18 17 17 17 62 61 64 66 164 166 165 168 167 
152 154 156 188 190 189 189 192 191 191 191 224 223 223 223 223 223 223 223 223 226
 225 225 228 227 86 85 85 85 85 85 85 85 85 85 85 88 87 90 260 259 262 264 263 68 7
0 72 71 71 71 2 4 3 3 6 5 5 5 5 5 5 14 16 15 15 15 15 15 15 15 18 17 17 182 181 184
 186 260 262 264 68 70 72 122 121 121 121 121 121 121 124 123 126 152 151 151 151 1
51 151 154 153 153 153 153 156 155 155 155 155 155 170 169 169 169 169 169 169 172 
171 174 173 173 260 262 264 263 263 263 263 218 217 217 217 217 217 217 217 217 217
 220 219 222 221 221 2 1 4 3 3 3 3 3 3 3 6 
 ```
 These numbers are called **transition-ids**. Type
 ```
 show-transitions data/lang/phones.txt exp/mono/0.mdl
```
what each transition-id stand for and its probability, for e.g.
```
Transition-state 1: phone = sil hmm-state = 0 pdf = 0
 Transition-id = 1 p = 0.5 [self-loop]
 Transition-id = 2 p = 0.5 [0 -> 1]  
Transition-state 2: phone = sil hmm-state = 1 pdf = 1
 Transition-id = 3 p = 0.5 [self-loop]
 Transition-id = 4 p = 0.5 [1 -> 2]
Transition-state 3: phone = sil hmm-state = 2 pdf = 2
 Transition-id = 5 p = 0.75 [self-loop]
 Transition-id = 6 p = 0.25 [2 -> 3]
 ...
Transition-state 142: phone = zh hmm-state = 0 pdf = 141
 Transition-id = 283 p = 0.75 [self-loop]
 Transition-id = 284 p = 0.25 [0 -> 1]
Transition-state 143: phone = zh hmm-state = 1 pdf = 142
 Transition-id = 285 p = 0.75 [self-loop]
 Transition-id = 286 p = 0.25 [1 -> 2]
Transition-state 144: phone = zh hmm-state = 2 pdf = 143
 Transition-id = 287 p = 0.75 [self-loop]
 Transition-id = 288 p = 0.25 [2 -> 3]
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
   
      
2. decriptions to MFCC feature extractions:      
   scripts and archives:     
   
   *.scp files map utterance if to position in *.ark files. The latter contains the actual data.    
   
   rspecifier:  **scp:feats.scp**  
   
   wspecifier:  **ark:mfcc.ark** to write to stdout. Archives will be written in binary; to avoid it append the **,t** modifier  **ark,t:mfcc.ark**
   
 
3. examinations of Monophone Model:
   view the HMM topology through 
   ```
   less data/lang/topo
   ```
   view the final monophone model:
   ```
   gmm-copy --binary=false exp/mono/final.mdl - | less
   ```
   which contains the above topology, Triples, DiagGMM.   
   view gmm summary:  
   ```
   gmm-info exp/mono/final.mdl
   ```  
   view some of the mixture Gaussians densities corresponding to cepstral coefficients:
   ```
   gmm-copy --binary=false exp/mono/final.mdl - | python local/plot_gmm.sh 
   ```
   
   
   
