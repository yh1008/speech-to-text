#!/bin/bash

[ -f path.sh ] && . ./path.sh

feats_nj=8
mfccdir=mfcc

echo ============================================================================
echo            "                Acoustic Data Preperation                    "
echo ============================================================================

./local/data_prep.sh

echo ============================================================================
echo          "                MFCC Feature Extration                    "
echo ============================================================================

mkdir conf
cp ../timit/s5/conf/mfcc.conf ./conf

for x in train test; do 
  steps/make_mfcc.sh --nj $feats_nj data/$x exp/make_mfcc/$x $mfccdir
  steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x $mfccdir
done

echo ============================================================================
echo            "                Language Model Creation                    "
echo ============================================================================

loc=`which ngram-count`;
if [ -z $loc ]; then
   if uname -a | grep 64 >/dev/null; then
      sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
   else
      sdir=$KALDI_ROOT/tools/srilm/bin/i686
   fi
   if [ -f $sdir/ngram-count ]; then
      echo "Using SRILM language modelling tool from $sdir"
      export PATH=$PATH:$sdir
   else
      echo "SRILM toolkit is probably not installed.
          Instructions: tools/install_srilm.sh"
      exit 1
   fi
fi
 
local=data/local
mkdir $local/tmp
ngram-count -order $lm_order -write-vocab $local/tmp/vocab-full.txt -wbdiscount -text $local/corpus.txt -lm $local/tmp/lm.arpa

echo ============================================================================
echo            "               Make G.fst                   "
echo ============================================================================

lang=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst
