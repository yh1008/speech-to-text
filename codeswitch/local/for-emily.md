```
yh2901@instance-1:~/kaldi/egs/codeswitch$ utils/fix_data_dir.sh data/train 
utils/fix_data_dir.sh: file data/train/utt2spk is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/text is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/segments is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/wav.scp is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/train/spk2gender is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: filtered data/train/segments from 50746 to 42463 lines based on filter /tmp/kaldi.ZCFy/recordings.
utils/fix_data_dir.sh: filtered data/train/wav.scp from 275 to 230 lines based on filter /tmp/kaldi.ZCFy/recordings.
utils/fix_data_dir.sh: filtered data/train/spk2gender from 148 to 147 lines based on filter /tmp/kaldi.ZCFy/speakers.
fix_data_dir.sh: kept 42463 utterances out of 50746
utils/fix_data_dir.sh: filtered data/train/spk2gender from 147 to 104 lines based on filter /tmp/kaldi.ZCFy/speakers.
fix_data_dir.sh: old files are kept in data/train/.backup
yh2901@instance-1:~/kaldi/egs/codeswitch$ utils/fix_data_dir.sh data/test
utils/fix_data_dir.sh: file data/test/utt2spk is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/test/text is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/test/segments is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/test/wav.scp is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: file data/test/spk2gender is not in sorted order or not unique, sorting it
utils/fix_data_dir.sh: filtered data/test/segments from 5400 to 3848 lines based on filter /tmp/kaldi.A4Ee/recordings.
utils/fix_data_dir.sh: filtered data/test/wav.scp from 20 to 17 lines based on filter /tmp/kaldi.A4Ee/recordings.
fix_data_dir.sh: kept 3848 utterances out of 5400
utils/fix_data_dir.sh: filtered data/test/spk2gender from 14 to 11 lines based on filter /tmp/kaldi.A4Ee/speakers.
fix_data_dir.sh: old files are kept in data/test/.backup
```
