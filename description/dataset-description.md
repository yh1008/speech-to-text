# [SEAME](https://catalog.ldc.upenn.edu/ldc2015s04) Dataset description 

### Ratio between transcribed words
Mandarin: 44%
English: 26% 
Silence: 21%
Others: 7%

### Data Summary
#### Sentences
Number of utterance: 54929  
Number of segmented utterance: 45872  
Number of unsegmented utterance: 9057  

#### Words
Based on the default parsing (2 space between Madarin chatacters and 1 space between English characters)    
Number of word: 518489  
Number of unique word: 28610  

Based on the processing (one step involves replacing non-transcribable sound (e.g., '[mm]') with sil symble which has space before and after (e.g., ' SIL1 '), and it will be able to help split some unsegmented phrases (e.g., '[mm]但是[mm]' (1 word in default) -> 'SIL1 但是 SIL1' (3 words after processing)))  
Number of word used: 534296  
Number of unique word used: 17531  
Number of unique word in filtered lexicon file: 11205  

Number of waste word type: 168  

### Transcription: special handling

1. Discourse particle: We use both English and Mandarin words to represent discourse particle. When the discourse occurs in Mandarin segment, we use words such as [啊], [喔], etc. to represent. When the discourse occurs in English segment, we use words such as [ah], [oh], etc. to represent.
2. Hesitation and filled pause: Filled pause refers to sounds made by people when they are hesitating/thinking. These sounds are indicated by a pair of brackets ( ), such as (er), (erm), etc.
3. Other languages: This group includes languages and dialects other than English and Mandarin. E.g, we find Japanese, Korean and Indian words. E.g, these words were spoken to describe food and places. In addition, the Chinese dialects such as Cantonese and Hokkien, can also be found in the recordings. These foreign language words are indicated by a pair of # within the word  e.g  
▪ #nasi-lemak# (a Malay word food dish):  
▪	#ah-mah#: It’s Hokkien dialect and it means “old woman”.   
▪	#ayumi-hamasaki#: a Japanese singer-songwriter.   
