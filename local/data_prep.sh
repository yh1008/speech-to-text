#!/bin/bash

cp -r ../wsj/s5/steps ./
cp -r ../wsj/s5/utils ./
./audio_data_prep.py
./acoustic_data_prep.py
