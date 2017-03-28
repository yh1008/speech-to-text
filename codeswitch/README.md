# codeswitch directory description

move this `codeswitch` directory under `kaldi/egs/`
```
cp codewitch ./kaldi/egs/
```
also put the `LDC2015S04` raw data folder under `kaldi/egs/codeswitch` 


### local
contains data preperation script and its README file 

### run.sh
contains the script to create MFCC feature extractions, (soon to be language model generation, tri-phone alignment, DNN and decode)

### path.sh 
tells where to find kaldi binary `. ./path.sh` is executed on all shell script to set the kaldi environment variable. 
to manually check if it is setted, use command
```
echo $KALDI_ROOT
```


