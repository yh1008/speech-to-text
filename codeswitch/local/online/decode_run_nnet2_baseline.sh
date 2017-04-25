#!/bin/bash
. cmd.sh
stage=1
train_stage=-10
use_gpu=false
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
  dir=exp/nnet2_online/tri22_nnet_a_gpu_baseline
  echo "using gpu 1"
else
  # Use 4 nnet jobs just like run_4d_gpu.sh so the results should be
  # almost the same, but this may be a little bit slow.
  num_threads=16
  minibatch_size=128
  parallel_opts="--num-threads $num_threads"
  dir=exp/nnet2_online/tri22_nnet_a_gpu_baseline
fi
if [ $stage -le 2 ]; then
    graph_dir=exp/tri22/graph
    # use already-built graphs.
    steps/nnet2/decode.sh --nj 14 --cmd "$decode_cmd" \
         $graph_dir data/test $dir/decode || exit 1;
fi
echo "finish decode online!"
