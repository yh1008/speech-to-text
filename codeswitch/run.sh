#!/bin/bash

[ -f path.sh ] && . ./path.sh

feats_nj=8
mono_nj = 8
tri_nj = 8
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

echo ============================================================================
echo            "               Monophone Training                   "
echo ============================================================================

steps/train_mono.sh --nj $mono_nj --cmd "$train_cmd" data/train data/lang exp/mono
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/mono exp/mono_ali
#utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graph
#steps/decode.sh --config conf/decode.config --nj $mono_nj --cmd "$decode_cmd" exp/mono/graph data/test exp/mono/decode

echo ============================================================================
echo            "               First Triphone Pass Training                   "
echo ============================================================================

steps/train_deltas.sh --cmd "$train_cmd" 2000 11000 data/train data/lang exp/mono_ali exp/tri1
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph #decoding
steps/decode.sh --config conf/decode.config --nj $tri_nj --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode

echo ============================================================================
echo            "                  Run.sh finished!                   "
echo ============================================================================
