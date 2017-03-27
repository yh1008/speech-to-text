#!/usr/bin/python3


__author__="Emily Hua"


import os
parent_path = os.path.split(os.getcwd())[0]
print (parent_path)


directory = parent_path + "/data/train"
if not os.path.exists(directory):
    os.makedirs(directory)

directory = parent_path + "/data/test"
if not os.path.exists(directory):
    os.makedirs(directory)

# a.) spk2gender 
# This file informs about speakers gender. As we assumed, 'speakerID' is a unique name of each speaker.
# 
# Pattern: [speakerID] [gender]

import os
audio_path = parent_path + '/LDC2015S04/seame_d2/data/interview/audio'
dir_list = os.listdir(audio_path)[1:]
import re
from collections import defaultdict 
id_dic = defaultdict(int)
for file in dir_list:
    id_dic[re.split('_', file)[0]] += 1
print ('there are {} unique speaker id'.format(len(id_dic)))


test_short_ids = ['01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB']
train_ids = []
test_ids = []
for key in id_dic:
    short_speaker_id = key[2:-1]
    if short_speaker_id not in test_short_ids:
        train_ids.append(key)
    else:
        test_ids.append(key)
print ('there are {} speaker ids in the training set'.format(len(train_ids)))
print ('there are {} speaker ids in the testing set'.format(len(test_ids)))


print (test_ids[:5])
print (train_ids[:5])

directory = parent_path + "/data/train/spk2gender"
with open(directory, 'w') as outfile:
    for speakerid in train_ids:
        outfile.write("{} {}\n".format(speakerid,speakerid[4]))

directory = parent_path + "/data/test/spk2gender"
with open(directory, 'w') as outfile:
    for speakerid in test_ids:
        outfile.write("{} {}\n".format(speakerid, speakerid[4]))

# b.) wav.scp 
# This file connects every utterance (sentence said by one person during particular recording session) with an audio file related to this utterance. If you stick to my naming approach, 'utteranceID' is nothing more than 'speakerID' (speaker's folder name) glued with *.wav file name without '.wav' ending (look for examples below).
# 
# Pattern: [recordingID] [full_path_to_audio_file]

directory = parent_path + "/data/train/wav.scp"
with open(directory, 'w') as outfile:
    for file in dir_list:
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids:
            path = parent_path + "/interview_audio/train/" + speaker_id + "/" + file
            outfile.write("{} flac -c -d -s {} |\n".format(re.split("\.", file)[0], path))

directory = parent_path + "/data/test/wav.scp"
with open(directory, 'w') as outfile:
    for file in dir_list:
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids:
            path = parent_path + "/interview_audio/test/" + speaker_id + "/" + file
            outfile.write("{} flac -c -d -s {} |\n".format(re.split("\.", file)[0], path))

# c.) text 
# This file contains every utterance matched with its text transcription.
# 
# Pattern: [uterranceID] [text_transcription]

trans_path = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript"
trans_list = os.listdir(trans_path)[1:]
directory = parent_path + "/data/train/text"
with open(directory, 'w') as outputfile:
    for file in trans_list: 
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids:
            trans_file = trans_path + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    text = re.split("\t", line)[-1]
                    prefix = re.split("\t", line)[0]
                    first_frame = re.split("\t", line)[1].zfill(7)
                    second_frame = re.split("\t", line)[2].zfill(7)
                    utterance_id = prefix + "_" + first_frame + "_" + second_frame
                    outputfile.write("{} {}".format(utterance_id, text))

trans_path = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript"
trans_list = os.listdir(trans_path)[1:]
directory = parent_path + "/data/test/text"
with open(directory, 'w') as outputfile:
    for file in trans_list: 
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids:
            trans_file = trans_path + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    text = re.split("\t", line)[-1]
                    prefix = re.split("\t", line)[0]
                    first_frame = re.split("\t", line)[1].zfill(7)
                    second_frame = re.split("\t", line)[2].zfill(7)
                    utterance_id = prefix + "_" + first_frame + "_" + second_frame
                    outputfile.write("{} {}".format(utterance_id, text))

# d.) utt2spk 
# This file tells the ASR system which utterance belongs to particular speaker.
# 
# Pattern: [uterranceID] [speakerID]

trans_path = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript/"
import sys
largest_frame = -sys.maxsize
trans_list = os.listdir(trans_path)[1:]
print ("there are {} recording with transcript".format(len(trans_list)))
print ("there are {} recording in audio files".format(len(dir_list)))
print ("match!")

for file in trans_list:
    file_path = trans_path + "/" + file
    with open(file_path, 'r') as inputfile:
        for line in inputfile:
            second_frame = int(re.split("\t", line)[2])
            if second_frame > largest_frame:
                largest_frame = second_frame
print ("largest_frame is {}".format(largest_frame))  
print ("since 7004497 is our largest frame, then we need to create string with 7 digits to hold all frames")

# create utterance id: recording id + start time + end time; for e.g. NI01MAX_0101_0001353_0003612
counter = 0
utter_ids = []
for file in trans_list:
    file_path = trans_path + "/" + file
    with open(file_path, 'r') as inputfile:
        for line in inputfile:
            speaker_id = re.split("_", line)[0]
            prefix = re.split("\t", line)[0]
            first_frame = re.split("\t", line)[1].zfill(7)
            second_frame = re.split("\t", line)[2].zfill(7)
            utterance_id =  prefix + "_" + first_frame + "_" + second_frame
            utter_ids.append(utterance_id)
print ("there are {} new utterance ids".format(len(utter_ids)))

print("sample newly created utterance id {}".format(utter_ids[:1]))

utt2spk_path = parent_path + "/data/train/utt2spk"
counter = 0
with open(utt2spk_path, 'w') as outputfile:
    for file in utter_ids:
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids:
            counter += 1
            outputfile.write("{} {}\n".format(re.split("\.", file)[0], speaker_id))
print ("there are {} in train/utt2spk".format(counter))

utt2spk_path = parent_path + "/data/test/utt2spk"
counter = 0
with open(utt2spk_path, 'w') as outputfile:
    for file in utter_ids:
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids:
            counter += 1
            outputfile.write("{} {}\n".format(re.split("\.", file)[0], speaker_id))
print ("there are {} in test/utt2spk".format(counter))

# e.) corpus.txt 
# This file has a slightly different directory. In kaldi-trunk/egs/digits/data create another folder local. In kaldi/egs/code-switching/data/local create a file corpus.txt which should contain every single utterance transcription that can occur in your ASR system (in our case it will be 100 lines from 100 audio files).
# 
# Pattern: [text_transcription]

temp_path = parent_path + "/data/local"
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
    
corpus_path = parent_path + "/data/local/corpus.txt"
trans_path = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript"
trans_list = os.listdir(trans_path)[1:]

with open(corpus_path, 'w') as outputfile:
    for file in trans_list: 
            trans_file = trans_path + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    #outputfile.write(line)
                    outputfile.write(re.split("\t", line)[3])


