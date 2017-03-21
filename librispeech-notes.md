# LIBRISPEECH Study


### Fixing Errors 
to avoid 
```
Please intall 'flac' on ALL worker nodes!
```
install flac codec:
```
sudo apt-get install flac
```

### Word-level Language Model
Look at the language model directory 
```
less data/lang/words.txt
```
shows
```
<eps> 0
!SIL 1
<SPOKEN_NOISE> 2
<UNK> 3
A 4
A''S 5
A'BODY 6
A'COURT 7
A'D 8
A'GHA 9
A'GOIN 10
A'LL 11
A'M 12
A'MIGHTY 13
A'MIGHTY'S 14
```
```
less data/lang/phones.txt
```
shows
```
<eps> 0
SIL 1
SIL_B 2
SIL_E 3
SIL_I 4
SIL_S 5
SPN 6
SPN_B 7
SPN_E 8
SPN_I 9
SPN_S 10
OY_B 11
OY_E 12
OY_I 13
OY_S 14
OY0_B 15
```
word boundries
```
less data/lang/phones/word_boundry.txt
```
shows
```
SIL nonword
SIL_B begin
SIL_E end
SIL_I internal
SIL_S singleton
SPN nonword
SPN_B begin
SPN_E end
SPN_I internal
SPN_S singleton
OY_B begin
OY_E end
OY_I internal
OY_S singleton
OY0_B begin
OY0_E end
OY0_I internal
OY0_S singleton
OY1_B begin
OY1_E end
OY1_I internal
OY1_S singleton
OY2_B begin
```
relates to the lexicon
```
less data/lang/phones/align_lexicon.txt
```
shows
```
!SIL !SIL SIL_S
<SPOKEN_NOISE> <SPOKEN_NOISE> SPN_S
<UNK> <UNK> SPN_S
<eps> <eps> SIL
A A AH0_S
A A EY1_S
A''S A''S EY1_B Z_E
A'BODY A'BODY EY1_B B_I AA2_I D_I IY0_E
A'COURT A'COURT EY1_B K_I AO2_I R_I T_E
A'D A'D EY1_B D_E
A'GHA A'GHA EY1_B G_I AH0_E
A'GOIN A'GOIN EY1_B G_I OY1_I N_E
A'LL A'LL EY1_B L_E
A'M A'M EY1_B M_E
A'MIGHTY A'MIGHTY EY1_B M_I AY1_I T_I IY0_E
A'MIGHTY'S A'MIGHTY'S EY1_B M_I AY1_I T_I IY0_I Z_E
A'MOST A'MOST EY1_B M_I OW2_I S_I T_E
A'N'T A'N'T EY1_B AH0_I N_I T_E
A'PENNY A'PENNY EY1_B P_I EH2_I N_I IY0_E
A'READY A'READY EY1_B R_I IY1_I D_I IY0_E
```
for word based language model, each utterance is mapped to a word instead of phones which we see in TIMIT
```
less data/train_10k/text
```
shows
```
103-1240-0002 FOR NOT EVEN A BROOK COULD RUN PAST MISSUS RACHEL LYNDE'S DOOR WIT
HOUT DUE REGARD FOR DECENCY AND DECORUM IT PROBABLY WAS CONSCIOUS THAT MISSUS RA
CHEL WAS SITTING AT HER WINDOW KEEPING A SHARP EYE ON EVERYTHING THAT PASSED FRO
M BROOKS AND CHILDREN UP
```
