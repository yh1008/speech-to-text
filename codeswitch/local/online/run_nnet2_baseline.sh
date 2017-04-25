#!/bin/bash

. cmd.sh


stage=1
train_stage=-10
use_gpu=false

tri_dir=tri2 # modify this to your intended tri* folder!

. cmd.sh
. ./path.sh
. ./utils/parse_options.sh

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
  # the _a is in case I want to change the parameters.
  dir=exp/nnet2_online/$tri_dir_nnet_a_gpu_baseline
  echo "using gpu 1"
else
  # Use 4 nnet jobs just like run_4d_gpu.sh so the results should be
  # almost the same, but this may be a little bit slow.
  num_threads=16
  minibatch_size=128
  parallel_opts="--num-threads $num_threads"
  dir=exp/nnet2_online/$tri_dir_nnet_a_baseline
fi



if [ $stage -le 1 ]; then
  # train without iVectors.
  steps/nnet2/train_pnorm_fast.sh --stage $train_stage \
    --num-epochs 8 --num-epochs-extra 4 \
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
    data/train data/lang exp/$tri_dir $dir  || exit 1;
fi

DEBUG=false
if ${DEBUG}; then
echo "this block is intended to be commented out"
if [ $stage -le 2 ]; then
    graph_dir=exp/$tri_dir/graph
    # use already-built graphs.
    steps/nnet2/decode.sh --nj 8 --cmd "$decode_cmd" \
         $graph_dir data/test $dir/decode || exit 1;
fi

if [ $stage -le 3 ]; then
  # If this setup used PLP features, we'd have to give the option --feature-type plp
  # to the script below.
  steps/online/nnet2/prepare_online_decoding.sh data/lang "$dir" ${dir}_online || exit 1;
fi


if [ $stage -le 4 ]; then
  # Decode.  The --per-utt true option makes no difference to the results here.
    graph_dir=exp/$tri_dir/graph
    steps/online/nnet2/decode.sh --cmd "$decode_cmd" --nj 8 \
        --per-utt true \
        "$graph_dir" data/test ${dir}_online/decode_utt || exit 1;
fi
echo "block ends"
fi
