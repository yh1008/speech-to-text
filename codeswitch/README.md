# codeswitch directory description

move this `codeswitch` directory under `kaldi/egs/`
```
cp codeswitch ./kaldi/egs/
```
also put the `LDC2015S04` raw data folder under `kaldi/egs/codeswitch` 


### run.sh
contains the script to prepare acoustic data and create MFCC feature extractions, (soon to be language model generation, tri-phone alignment, DNN and decode)
to execute:
```
./run.sh
```

### local
contains data preperation script and its README file   
to execute:
```
chmod 755 local/audio_data_prep.py
chmod 755 local/acoustic_data_prep.py

./local/audio_data_prep.py
./local/acoustic_data_prep.py
```


### path.sh 
tells where to find kaldi binary `. ./path.sh` is executed on all shell script to set the kaldi environment variable. 
to manually check if it is setted, use command
```
echo $KALDI_ROOT
```


