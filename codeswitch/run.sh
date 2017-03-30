#!/bin/bash

[ -f path.sh ] && . ./path.sh

feats_nj=8
mfccdir=mfcc

echo ============================================================================
echo            "                Data Preperation                    "
echo ============================================================================

./local/data_prep.sh

echo ============================================================================
echo          "                MFCC Feature Extration                    "
echo ============================================================================

mkdir conf
cp ../timit/s5/conf/mfcc.conf ./conf
steps/make_mfcc.sh --nj $feats_nj data/train exp/make_mfcc/train $mfccdir
steps/make_mfcc.sh --nj $feats_nj data/test exp/make_mfcc/test $mfccdir

steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfccdir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir
