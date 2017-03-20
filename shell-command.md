# Useful Shell Command to deal with Kaldi

### to set KALDI_ROOT environment variable 
```
source path.sh
```
or equivalently
```
. ./path.sh
```
where **path.sh** set KALDI_ROOT to point to the Kaldi installation

### where is the environment variable that tells the problem where Kaldi binary is?
```
echo KALDI_ROOT
```

### check if a file exists if not preceed to the next
```
[ -f ./path.sh ] && . ./path.sh
```

### **less**: view a file and not edit it
```
less sa1.phn
```

### **wc -l**: count number of lines in a file
```
wc -l < data/train/utt2spk
```
### check the dimensionality of MFCC features
```
feat-to-dim scp:data/train/feats.scp -
feat-to-dim ark:mfcc/raw_mfcc_train.1.ark -
```

### **grep** search for a string in a file 
```
grep falr0_sx335 feats.scp 
```

### check how many frames that utterance has?
```
feat-to-len 
```
feat-to-len: reads an archive of features and writes a corresponding archive
that maps utterance-id to utterance length in frames, or (with
one argument) print to stdout the total number of frames in the
input archive.  
Usage: feat-to-len [options] \<in-rspecifier> [\<out-wspecifier>]
e.g.: feat-to-len scp:feats.scp ark,t:feats.lengths
or: feat-to-len scp:feats.scp  

### write the MFCC features to stdout 
```
copy-feats scp:data/train/feats.scp ark,t:- | head
```
the archives by default are written in binary, in order to view it with human eyes, we use **copy-feats** make a copy and write to stdout with the suitable wspecifier.   

### **--nj** specifies number of parallel jobs
```
steps/train_mono.sh --nj 4 data/train data/lang exp/mono
```
The option **--nj 4** instructs Kaldi to split computation into four parallel jobs. And there needs to be >= number of CPUs which are not in use.   

### check how many phones are in the language model
```
wc -l < data/lang/phones.txt
```

### get summary information of mono model 
```
gmm-info exp/mono/final.mdl
```  
get
```
gmm-info exp/mono/final.mdl 
number of phones 48
number of pdfs 144
number of transition-ids 288
number of transition-states 144
feature dimension 39
number of gaussians 986
```
