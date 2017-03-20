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
