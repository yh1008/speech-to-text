#!/bin/bash

[ -f path.sh ] && . ./path.sh

echo ============================================================================
echo "                MFCC Feature Extration                    "
echo ============================================================================
mkdir conf
cp ../timit/s5/conf/mfcc.conf ./conf
steps/make_mfcc.sh --nj 8 data/train exp/make_mfcc/train mfcc
steps/make_mfcc.sh --nj 8 data/test exp/make_mfcc/test mfcc

steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train mfcc
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test mfcc
