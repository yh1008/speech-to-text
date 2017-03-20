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
