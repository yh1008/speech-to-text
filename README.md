### Mixlingual Speech-To-Text project

From the team:   
As Chinese students studying in the states, we found our speaking habits morphed -- English words and phrases easily get slipped into Chinese sentences. We greatly feel the need to have messaging apps that can handle multilingual speech-to-text translation. So in this task, we are going to develop this function -- build a model using deep learning technologies to corretly translate multilingual audio (having Chinese and English in the same sentence) into text.

Model breakdown:  
M1: language detection model  
M2: Mandarin speech-to-text model  
M3: English speech-to-text model       
  
Data Preperation: http://kaldi-asr.org/doc/kaldi_for_dummies.html  
  
| acoustic data:  | filename: | pattern: |path: | source:|
| ------------- | ------------- |-|--|--|
|  |spk2gender  |\<speakerID>\<gender> | /data/train /data/test | handmade|
|  | utt2spk    |\<utteranceID>\<speakerID> | /data/train /data/test| handmade | 
|  | wav.scp    |\<utteranceID>\<full_path_to_audio_file>|/data/train /data/test | handmade|
|  | text       |\<utteranceID>\<full_path_to_audio_file> | /data/train /data/test|  exists | 
|language data:  | lexicon.txt |\<word> \<phone 1>\<phone 2> ... |data/local/dict| egs/voxforge|
|  | nonsilence_phones.txt | \<phone>|data/local/dict | unkown | 
|  |silence_phones.txt   |\<phone> |data/local/dict |unkown |
|  | optional_silence.txt |\<phone> | data/local/dict| unkown | 
|Tools:  | utils | |/ | kaldi/egs/wsj/s5| 
|  |steps  |  |/ | kaldi/egs/wsj/s5 |
|  | score.sh |  | /| kaldi/egs/voxforge/s5/local | 

