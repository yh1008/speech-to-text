# [SEAME](https://catalog.ldc.upenn.edu/ldc2015s04) Dataset description 

### Ratio between transcribed words
Mandarin: 44%
English: 26% 
Silence: 21%
Others: 7%

### Data Summary
Number of utterance: 54929
Number of utterance with unparsed elements: 204
Number of utterance with non-transcribable sounds: 8823

Based on the default parsing (2 space between Madarin chatacters and 1 space between English characters)
Number of word: 28614
Number of non-transcribable sound word: 12450
Number of word filtered out by CMU dictionary (all English words): 8639

### Transcription: special handling

1. Discourse particle: We use both English and Mandarin words to represent discourse particle. When the discourse occurs in Mandarin segment, we use words such as [啊], [喔], etc. to represent. When the discourse occurs in English segment, we use words such as [ah], [oh], etc. to represent.
2. Hesitation and filled pause: Filled pause refers to sounds made by people when they are hesitating/thinking. These sounds are indicated by a pair of brackets ( ), such as (er), (erm), etc.
3. Other languages: This group includes languages and dialects other than English and Mandarin. E.g, we find Japanese, Korean and Indian words. E.g, these words were spoken to describe food and places. In addition, the Chinese dialects such as Cantonese and Hokkien, can also be found in the recordings. These foreign language words are indicated by a pair of # within the word  e.g  
▪ #nasi-lemak# (a Malay word food dish):  
▪	#ah-mah#: It’s Hokkien dialect and it means “old woman”.   
▪	#ayumi-hamasaki#: a Japanese singer-songwriter.   
