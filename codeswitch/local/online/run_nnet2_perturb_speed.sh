#!/bin/bash

. ./cmd.sh
. ./path.sh

stage=-1
train_stage=-10
use_gpu=false
nnet_dir=exp/nnet2_online_perturb

if $use_gpu; then
  if ! cuda-compiled; then
    cat <<EOF && exit 1
This script is intended to be used with GPUs but you have not compiled Kaldi with CUDA
If you want to use GPUs (and have them), go to src/, and configure and make on a machine
where "nvcc" is installed.  Otherwise, call this script with --use-gpu false
EOF
  fi
  parallel_opts="--gpu 1"
  num_threads=1
  minibatch_size=512
  dir=$nnet_dir/nnet_a_gpu
else
  num_threads=16
  minibatch_size=128
  parallel_opts="--num-threads $num_threads"
  dir=$nnet_dir/nnet_a
fi

echo ============================================================================
echo            "                Stage -1                    "
echo ============================================================================
if [ $stage -le -1 ]; then
  utils/perturb_data_dir_speed.sh 0.9 data/train data/train_per1
  utils/perturb_data_dir_speed.sh 1.0 data/train data/train_per2
  utils/perturb_data_dir_speed.sh 1.1 data/train data/train_per3
  utils/combine_data.sh data/train_per data/train_per1 data/train_per2 data/train_per3
  rm -r data/train_per1 data/train_per2 data/train_per3
  mfccdir=mfcc_perturbed

 for x in train_per; do
    steps/make_mfcc.sh --cmd "$train_cmd" --nj 20 \
      data/$x exp/make_mfcc/$x $mfccdir || exit 1;
    steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x $mfccdir || exit 1;
  done

fi

echo ============================================================================
echo            "                Stage 0                    "
echo ============================================================================

if [ $stage -le 0 ]; then
  steps/align_fmllr.sh --nj 30 --cmd "$train_cmd" \
    data/train_per data/lang exp/tri4 exp/tri4_ali || exit 1;
fi

echo ============================================================================
echo            "                Stage 1                    "
echo ============================================================================

if [ $stage -le 1 ]; then
  mkdir -p $nnet_dir
  steps/online/nnet2/train_diag_ubm.sh --cmd "$train_cmd" --nj 30 --num-frames 200000 \
    data/train_per 256 exp/tri3 $nnet_dir/diag_ubm
fi	

echo ============================================================================
echo            "                Stage 2                    "
echo ============================================================================

if [ $stage -le 2 ]; then
  steps/online/nnet2/train_ivector_extractor.sh --cmd "$train_cmd" --nj 10 \
    data/train_per $nnet_dir/diag_ubm $nnet_dir/extractor || exit 1;
fi

echo ============================================================================
echo            "                Stage 3                    "
echo ============================================================================

if [ $stage -le 3 ]; then
   steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 30 \
    data/train_per $nnet_dir/extractor $nnet_dir/ivectors_train_per || exit 1;
fi

echo ============================================================================
echo            "                Stage 4                    "
echo ============================================================================

if [ $stage -le 4 ]; then
  steps/nnet2/train_pnorm_simple2.sh --stage $train_stage \
    --online-ivector-dir $nnet_dir/ivectors_train_per \
    --num-epochs 4 \
    --splice-width 7 --feat-type raw \
    --cmvn-opts "--norm-means=false --norm-vars=false" \
    --num-threads "$num_threads" \
    --minibatch-size "$minibatch_size" \
    --parallel-opts "$parallel_opts" \
    --num-jobs-nnet 6 \
    --num-hidden-layers 4 \
    --mix-up 4000 \
    --initial-learning-rate 0.02 --final-learning-rate 0.004 \
    --cmd "$decode_cmd" \
    --pnorm-input-dim 2400 \
    --pnorm-output-dim 300 \
    data/train_per data/lang exp/tri4_ali $dir  || exit 1;
fi

echo ============================================================================
echo            "                Stage 5                    "
echo ============================================================================

if [ $stage -le 5 ]; then
    steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 8 \
      data/test $nnet_dir/extractor $nnet_dir/ivectors_test || exit 1;
fi

echo ============================================================================
echo            "                Stage 6                    "
echo ============================================================================

if [ $stage -le 6 ]; then
    graph_dir=exp/tri4/graph
    steps/nnet2/decode.sh --nj 8 --cmd "$decode_cmd" \
        --online-ivector-dir $nnet_dir/ivectors_test \
        $graph_dir data/test $dir/decode || exit 1;
fi

