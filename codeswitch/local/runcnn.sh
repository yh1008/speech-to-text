#!/bin/bash

[ -f path.sh ] && . ./path.sh
[ -f cmd.sh ] && . ./cmd.sh

feats_nj=8
mono_nj=8
tri_nj=8
decode_nj=7
fbankdir=fbank

chmod +x local/score.sh
echo ============================================================================
echo            "                Acoustic Data Preperation                    "
echo ============================================================================

cd local
chmod +x data_prep.sh
./data_prep.sh

echo ============================================================================
echo          "                FBank Feature Extration                    "
echo ============================================================================

cd ../
conf_dir=conf
if [[ ! -e $conf_dir ]]; then
    mkdir $conf_dir
elif [[ ! -d $conf_dir ]]; then
    echo "$conf_dir already exists but is not a directory" 1>&2
fi
cp ../chime4/s5_1ch/conf/fbank.conf ./$conf_dir

utils/fix_data_dir.sh data/train
for x in train test; do 
  steps/make_fbank.sh --nj $feats_nj data/$x exp/make_fbank/$x $fbankdir
  steps/compute_cmvn_stats.sh data/$x exp/make_fbank/$x $fbankdir
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
lm_order=3
ngram-count -order $lm_order -write-vocab $local/tmp/vocab-full.txt -wbdiscount -text $local/corpus.txt -lm $local/tmp/lm.arpa
echo "created language model"

echo ============================================================================
echo            "               Make G.fst                   "
echo ============================================================================

lang=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst

echo ============================================================================
echo            "               Monophone Training                   "
echo ============================================================================

steps/train_mono.sh --nj $mono_nj --cmd "$train_cmd" data/train data/lang exp/mono
steps/align_si.sh --nj $mono_nj --cmd "$train_cmd" data/train data/lang exp/mono exp/mono_ali
#utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graph
#steps/decode.sh --config conf/decode.conf --nj $decode_nj --cmd "$decode_cmd" exp/mono/graph data/test exp/mono/decode

echo ============================================================================
echo            "               First Triphone Pass Training                   "
echo ============================================================================

steps/train_deltas.sh --cmd "$train_cmd" 1000 11000 data/train data/lang exp/mono_ali exp/tri1
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph #decoding
#steps/decode.sh --config conf/decode.conf --nj $decode_nj --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode
#local/score.sh --cmd run.pl data/test exp/tri1/graph exp/tri1/decode

echo ============================================================================
echo            "               Tri2: LDA+MLLT                  "
echo ============================================================================

steps/align_si.sh --nj $tri_nj --cmd "$train_cmd" --use-graphs true data/train data/lang exp/tri1 exp/tri1_ali
steps/train_lda_mllt.sh --cmd "$train_cmd" --splice-opts "--left-context=3 --right-context=3" 1000 11000 data/train data/lang exp/tri1_ali exp/tri2
utils/mkgraph.sh data/lang exp/tri2 exp/tri2/graph 
#steps/decode.sh --config conf/decode.conf --nj $decode_nj --cmd "$decode_cmd" exp/tri2/graph data/test exp/tri2/decode
steps/align_si.sh --nj $tri_nj --cmd "$train_cmd" --use-graphs true data/train data/lang exp/tri2 exp/tri2a_ali #simple algin
#local/score.sh --cmd run.pl data/test exp/tri2/graph exp/tri2/decode

echo ============================================================================
echo            "      Tri2b: Align LDA-MLLT triphones with FMLLR           "
echo ============================================================================

steps/align_fmllr.sh --nj $tri_nj --cmd run.pl  data/train data/lang exp/tri2 exp/tri2b_ali # FMLLR align

echo ============================================================================
echo            "      Tri3: SAT Aligned with FMLLR           "
echo ============================================================================

steps/train_sat.sh --cmd "$train_cmd" 1000 11000 data/train data/lang exp/tri2b_ali exp/tri3
steps/align_fmllr.sh --cmd "$train_cmd" data/train data/lang exp/tri3 exp/tri3_ali
utils/mkgraph.sh data/lang exp/tri3 exp/tri3/graph 
#steps/decode_fmllr.sh --nj $decode_nj --cmd "$decode_cmd" exp/tri3/graph data/test exp/tri3/decode
#local/score.sh --cmd run.pl data/test exp/tri3/graph exp/tri3/decode

echo ============================================================================
echo            "                  Preparation finished!                   "
echo ============================================================================



dev=data/test
train=data/train


gmm=exp/tri2a

stage=0
. utils/parse_options.sh

set -euxo pipefail

# Make the FBANK features,
#[ ! -e $dev ] && if [ $stage -le 0 ]; then
#  # Dev set
#  utils/copy_data_dir.sh $dev_original $dev || exit 1; rm $dev/{cmvn,feats}.scp
#  steps/make_fbank_pitch.sh --nj 10 --cmd "$train_cmd" \
#     $dev $dev/log $dev/data || exit 1;
#  steps/compute_cmvn_stats.sh $dev $dev/log $dev/data || exit 1;
#  # Training set
#  utils/copy_data_dir.sh $train_original $train || exit 1; rm $train/{cmvn,feats}.scp
#  steps/make_fbank_pitch.sh --nj 10 --cmd "$train_cmd" \
#     $train $train/log $train/data || exit 1;
#  steps/compute_cmvn_stats.sh $train $train/log $train/data || exit 1;
#  # Split the training set
#  
#fi

echo ============================================================================
echo            "                  split cv                   "
echo ============================================================================


# split cv
utils/subset_data_dir_tr_cv.sh --cv-spk-percent 10 $train ${train}_tr90 ${train}_cv10

echo ============================================================================
echo            "                  CNN pre-training                   "
echo ============================================================================


# Run the CNN pre-training,
hid_layers=2
if [ $stage -le 1 ]; then
  dir=exp/cnn4c
  ali=${gmm}_ali
  # Train
  $train_cmd $dir/log/train_nnet.log \
    steps/nnet/train.sh \
      --cmvn-opts "--norm-means=true --norm-vars=true" \
      --delta-opts "--delta-order=2" --splice 5 \
      --network-type cnn1d --cnn-proto-opts "--patch-dim1 8 --pitch-dim 3" \
      --hid-layers $hid_layers --learn-rate 0.008 \
      --skip-cuda-check false \
      ${train}_tr90 ${train}_cv10 data/lang $ali $ali $dir || exit 1;
  # Decode,
  steps/nnet/decode.sh --nj $decode_nj --cmd "$decode_cmd" --config conf/decode_dnn.conf --acwt 0.1 \
    $gmm/graph $dev $dir/decode || exit 1;
fi

echo ============================================================================
echo     "    Concat 'feature_transform' with convolutional layers             "
echo ============================================================================



if [ $stage -le 2 ]; then
  # Concat 'feature_transform' with convolutional layers,
  dir=exp/cnn4c
  nnet-concat $dir/final.feature_transform \
    "nnet-copy --remove-last-components=$(((hid_layers+1)*2)) $dir/final.nnet - |" \
    $dir/final.feature_transform_cnn
fi

echo ============================================================================
echo     "    Pre-train stack of RBMs on top of the convolutional layers (4 layers, 1024 units)          "
echo ============================================================================

# Pre-train stack of RBMs on top of the convolutional layers (4 layers, 1024 units),
if [ $stage -le 3 ]; then
  dir=exp/cnn4c_pretrain-dbn
  transf_cnn=exp/cnn4c/final.feature_transform_cnn # transform with convolutional layers
  # Train
  $train_cmd $dir/log/pretrain_dbn.log \
    steps/nnet/pretrain_dbn.sh --nn-depth 4 --hid-dim 1024 --rbm-iter 20 \
    --feature-transform $transf_cnn --input-vis-type bern \
    --param-stddev-first 0.05 --param-stddev 0.05 \
    $train $dir || exit 1
fi

echo ============================================================================
echo     "    Re-align using CNN          "
echo ============================================================================

# Re-align using CNN,
if [ $stage -le 4 ]; then
  dir=exp/cnn4c
  steps/nnet/align.sh --nj $tri_nj --cmd "$train_cmd" \
    $train data/lang $dir ${dir}_ali || exit 1
fi

echo ============================================================================
echo     "    Train the DNN optimizing cross-entropy         "
echo ============================================================================

# Train the DNN optimizing cross-entropy,
if [ $stage -le 5 ]; then
  dir=exp/cnn4c_pretrain-dbn_dnn; [ ! -d $dir ] && mkdir -p $dir/log;
  ali=exp/cnn4c_ali
  feature_transform=exp/cnn4c/final.feature_transform
  feature_transform_dbn=exp/cnn4c_pretrain-dbn/final.feature_transform
  dbn=exp/cnn4c_pretrain-dbn/4.dbn
  cnn_dbn=$dir/cnn_dbn.nnet
  { # Concatenate CNN layers and DBN,
    num_components=$(nnet-info $feature_transform | grep -m1 num-components | awk '{print $2;}')
    cnn="nnet-copy --remove-first-components=$num_components $feature_transform_dbn - |"
    nnet-concat "$cnn" $dbn $cnn_dbn 2>$dir/log/concat_cnn_dbn.log || exit 1 
  }
  # Train
  $train_cmd $dir/log/train_nnet.log \
    steps/nnet/train.sh --feature-transform $feature_transform --dbn $cnn_dbn --hid-layers 0 \
    ${train}_tr90 ${train}_cv10 data/lang $ali $ali $dir || exit 1;
  # Decode (reuse HCLG graph)
  steps/nnet/decode.sh --nj $decode_nj --cmd "$decode_cmd" --config conf/decode_dnn.conf --acwt 0.1 \
    $gmm/graph $dev $dir/decode || exit 1;
fi



echo ============================================================================
echo     "    generate lattices and alignments        "
echo ============================================================================

# Sequence training using sMBR criterion, we do Stochastic-GD with per-utterance updates.
# Note: With DNNs in RM, the optimal LMWT is 2-6. Don't be tempted to try acwt's like 0.2, 
# the value 0.1 is better both for decoding and sMBR.
dir=exp/cnn4c_pretrain-dbn_dnn_smbr
srcdir=exp/cnn4c_pretrain-dbn_dnn
acwt=0.1

# First we generate lattices and alignments,
if [ $stage -le 6 ]; then
  steps/nnet/align.sh --nj $tri_nj --cmd "$train_cmd" \
    $train data/lang $srcdir ${srcdir}_ali || exit 1;
  steps/nnet/make_denlats.sh --nj $decode_nj --cmd "$decode_cmd" --config conf/decode_dnn.conf --acwt $acwt \
    $train data/lang $srcdir ${srcdir}_denlats || exit 1;
fi

echo ============================================================================
echo     "    Re-train the DNN by 6 iterations of sMBR      "
echo ============================================================================

# Re-train the DNN by 6 iterations of sMBR,
if [ $stage -le 7 ]; then
  steps/nnet/train_mpe.sh --cmd "$train_cmd" --num-iters 6 --acwt $acwt --do-smbr true \
    $train data/lang $srcdir ${srcdir}_ali ${srcdir}_denlats $dir || exit 1
  # Decode
  for ITER in 1 3 6; do
    steps/nnet/decode.sh --nj $decode_nj --cmd "$decode_cmd" --config conf/decode_dnn.conf \
      --nnet $dir/${ITER}.nnet --acwt $acwt \
      $gmm/graph $dev $dir/decode_it${ITER} || exit 1
  done 
fi

echo Success
exit 0
