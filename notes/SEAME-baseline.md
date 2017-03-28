# [SEAME baseline paper](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6289015) 

### The baseline ASR system in the paper: 
Achieves 37.2% MER

Adapt the Cambridge pronunciation dictionary for Singaporean accent: following three rules are used: 
1. syllable-final voiceless plosive omitted if preceded by another consonant: /p/, /t/, /k/ might be deleted 
word-fins; 
2. /t/, /d/ omitted if preceded by another consonant: /t/, /d/ might be deleted 
3. word-final metathesis from ‘sp’ to ‘ps’ 


trigram language model:
build from the SEAME training transcriptions containing the full 16k-vocabulary of the transcriptions. Those models were interpolated with two monolingual language models. The interpolation weights were tuned on the transcriptions of the SEAME development set by minimizing the perplexity of the model. Supplemental vocabulary was selected from CH-mono and EN-mono by selecting frequent words which are not in the transcriptions. The total vocabulary size is 30k words. 

don’t perform phone merging: 
cause phone merging results in a higher confusion between words of different languages during decoding 
