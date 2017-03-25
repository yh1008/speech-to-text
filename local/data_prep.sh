#!/bin/bash

cp -r ../timit/s5/utils ./
cp -r ../timit/s5/steps ./
./audio_data_prep.py
./acoustic_data_prep.py
