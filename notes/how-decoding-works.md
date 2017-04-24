# How decoding works

Things you need:

```javascript
# INPUT:
#    transcriptions/
#        wav.scp
#
#    config/
#        mfcc.conf
#
#    experiment/
#        triphones_deldel/
#            final.mdl
#
#            graph/
#                HCLG.fst
#                words.txt
```

* The only file that needs to be made for the new audio files
* A configuration file specifying how to extract MFCCs
* A trained DNN acoustic model final.mdl
* A compiled decoding graph HCLG.fst: it combines the acoustic model (HC), the pronunciation dictionary (lexicon), and the language model (G)
* A mapping of word-IDs to words words.txt: HCLG.fst uses the integers representing words. As such, words.txt maps from the list of integers we get from decoding to something readable

For example, I’m just going to decode one audio file, so my wav.scp file is one line long. It will be a two-column file, with the utterance ID on the left column and the path to the audio file on the right column. It looks like this:

```javascript
$cat wav.scp 
atai_45 input/audio/atai_45.wav
```

Except wav.scp, all the other files should have already been created during the training phrase.
