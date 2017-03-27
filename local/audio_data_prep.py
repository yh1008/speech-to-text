#!/usr/bin/python3

__author__="Emily Hua"

import os
parent_path = os.path.split(os.getcwd())[0]
print (parent_path)

audio_path = parent_path + '/LDC2015S04/seame_d2/data/interview/audio'
dir_list = os.listdir(audio_path)[1:]
print ("there are total {} of files in {}".format(len(dir_list), audio_path))

##################################
#### create train and test set ###
##################################
import re
from collections import defaultdict 
id_dic = defaultdict(int)
for file in dir_list:
    id_dic[re.split('_', file)[0][2:-1]] += 1
print ('there are {} unique prefix sets'.format(len(id_dic)))


test_ids = ['01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB']


train_ids = []
for key in id_dic:
    if key not in test_ids:
        train_ids.append(key)
print ('there are {} speaker ids in the training set'.format(len(train_ids)))

print("ids in training set {}".format(train_ids))

test_wannabe = []
for file in dir_list:
    speaker_id = re.split('_', file)[0][2:-1]
    if speaker_id in test_ids:
        test_wannabe.append(file)
        # I have add a file from this prefix into the test set, no need for more from this prefix
print ("there are {} files ready to be moved into the test set, should equal 16 by the way".format(len(test_wannabe)))


directory = parent_path + "/interview_audio"
if not os.path.exists(directory):
    os.makedirs(directory)
print (directory)


from shutil import copyfile
directory += "/test"
print ("loading audios into {}".format(directory))
if not os.path.exists(directory):
    os.makedirs(directory)
    for file in test_wannabe:
        speaker_id = re.split('_',file)[0][2:-1]
        if not os.path.exists(directory + "/" + speaker_id):
            os.makedirs(directory + "/" + speaker_id)
        src = audio_path + "/" + file
        dst = directory + "/" + speaker_id + "/" + file
        copyfile(src, dst)
print ("loading finished")

# @train_ids stores speaker that is supposed to be in the train set
from shutil import copyfile
directory = parent_path + "/interview_audio"
directory += "/train"
print ("loading audios into {}".format(directory))
if not os.path.exists(directory):
    os.makedirs(directory)
    for file in dir_list:
        speaker_id = re.split('_',file)[0][2:-1]
        if speaker_id in train_ids:
            if not os.path.exists(directory + "/" + speaker_id):
                os.makedirs(directory + "/" + speaker_id)
            src = audio_path + "/" + file
            dst = directory + "/" + speaker_id + "/" + file
            copyfile(src, dst)
print ("loading finished")



