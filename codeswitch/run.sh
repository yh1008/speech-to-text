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
