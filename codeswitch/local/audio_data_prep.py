#!/usr/bin/env python3

"""This is the main module that structures the audio directory for Kaldi to consume
   This script will prepare the audio directory as audio/<test || train>/<speaker id>/<recording>
   e.g. audio/train/NC03FBX/NC03FBX_020101.flac
"""
__author__="Emily Hua"

import re
import os
import glob
from shutil import copyfile
from shutil import rmtree
from collections import defaultdict 

def get_file_list(audio_path, dirn):
    r"""Count the number of recordings in Conversation and Interview directories, return a list of file names
    Returns
    -------
    dir_list : list
        a list of file names under the corresponding Conversation or Interview's audio directory
    """
    dir_list = os.listdir(audio_path)
    dir_list = [f for f in os.listdir(audio_path) if re.match(r'[^\\]+\.flac', f)] # makes sure unwanted files like .DS_Store doesn't show up here! 
    print ("there are total {} of files in {}\n".format(len(dir_list), audio_path))
    if dirn == 'interview':
        assert (len(dir_list) == 210), 'LDC2015S04/seame_d1/data/interview/audio should have 210 recordings, check if the directory is corrupted'
    else:
        assert (len(dir_list) == 87), 'LDC2015S04/seame_d2/data/conversation/audio should have 87 recordings, check if the directory is corrupted'
    return dir_list

def speaker_re_counts(dir_list):
    r"""Create a dictionary mapping of prefix to the number of recordings under this prefix. 
    Returns
    -------
    id_dic : collections.defaultdict
        a dictionary with key as recording prefix (tentative speaker id) and number of files associated with this prefix
        e.g. (interview) 'NI52MBQ': 2
        e.g. (conversation) '37NC45MBP': 1
    """
    id_dic = defaultdict(int)
    for file in dir_list:
        id_dic[re.split('_', file)[0]] += 1
    return id_dic

def train_test_split(id_dic, test_short_ids, dirn):
    r"""generate a list of speaker id that should be the train or test set 
    Returns
    -------
    train_ids, test_ids : list, list
        a list of ids that belong to train or test set 
        e.g. (interview train) 'NI52MBQ' (interview test) 'NI55FBP'
        e.g. (conversation train) '37NC45MBP' (interview test) '01NC02FBY'
    """
    train_ids = []
    test_ids = []
    for key in id_dic:
        if key[2:-1] in test_short_ids or key[:-1] in test_short_ids:
            test_ids.append(key)
        else: 
            train_ids.append(key)
    print ('there are {} unprocessed speaker ids in the training set'.format(len(train_ids)))
    print ('there are {} unprocessed speaker ids in the testing set\n'.format(len(test_ids)))
    
    if dirn == "interview":
        assert (len(train_ids) == 85 and len(test_ids) == 10), "For interview, there should be 85 speakers be moved to the training set, 10 speakers in test set"
    else:
        assert (len(train_ids) == 75 and len(test_ids) == 4), "For conversation, there should be 75 speakers be moved to the training set, 4 speakers in test set"
    
    return train_ids, test_ids


def create_test_wannabe(dir_list, test_ids, dirn):
    r"""generate a list of recording file name that should be moved to the test set 
    Returns
    -------
    test_wannabe : list
        a list of file names that we moved to test set
        e.g. (interview) 'NI01MAX_0101.flac'
        e.g. (conversation) '01NC01FBX_0101.flac'
    """
    test_wannabe = []
    for file in dir_list:
        speaker_id = re.split('_', file)[0]
        if speaker_id in test_ids:
            test_wannabe.append(file)
    print ("there are {} files ready to be moved into the test set".format(len(test_wannabe)))
    if dirn == "interview":
        assert (len(test_wannabe) == 16), "16 files from interview should be moved into the test set"
    else:
        assert (len(test_wannabe) == 4), "4 files from conversation should be moved into the test set"    
    return test_wannabe


def clean_up (dir_path):
    files = glob.glob(dir_path+'/*')
    for f in files:
        rmtree(f)

def load_audios_to_test(test_files_list,audio_path, dirn):
    counter = 0
    directory = parent_path + "/audio"
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory += "/test"
    print ("\nloading {} recordings into {}".format(dirn, directory))
    
    if not os.path.exists(directory):
        os.makedirs(directory)        
    for file in test_files_list:
        src = audio_path + "/" + file
        if dirn == "interview":
            speaker_id = re.split('_',file)[0]
        elif dirn =="conversation":
            speaker_id = re.split('_',file)[0][2:]
            file = file[2:]
        if not os.path.exists(directory + "/" + speaker_id):
            os.makedirs(directory + "/" + speaker_id)
        dst = directory + "/" + speaker_id + "/" + file
        copyfile(src, dst)
        counter += 1
    if dirn == "interview":
        assert (counter == 16), "should move 16 interview files to test folder, the number mismatched, investigate!"
    else:
        assert (counter == 4), "should move 4 conversation files to test folder, the number mismatched, investigate!"
    print ("loading {} to test finished!".format(dirn))


def load_interview_train(dir_list):
    r""" loading corresponding interview recordings to the training directory 
    Returns
    -------
    None
    """
    directory = parent_path + "/audio"
    directory += "/train"
    print ("\nloading interview recordings into {}".format(directory))
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        clean_up(directory) # remove whatever is already in the train directory
    
    for file in dir_list:
        speaker_id = re.split('_',file)[0]
        if speaker_id in train_ids_i:
            if not os.path.exists(directory + "/" + speaker_id):
                os.makedirs(directory + "/" + speaker_id)
            src = audio_path_i + "/" + file
            dst = directory + "/" + speaker_id + "/" + file
            copyfile(src, dst)
    print ("loading finished")


def get_speaker_multiple(ids):
    r"""generate a list of recording prefix which recordings need to be renamed 
    Returns
    -------
    speaker_multiple : list
        a list of speaker ids that have multiple files under its name, and need to be renamed 
    """
    speaker_multiple = []
    sets = set([])
    for i in ids:
        sets.add(i[2:])
    dic = defaultdict(list)
    for file in dir_list_c:
        dic[re.split("_",file)[0][2:]].append(file)
    for key in dic:
        if len(dic[key]) > 1 :
            speaker_multiple.append(key)
    print ("speakers with multiple recordings:\n {}".format(speaker_multiple))
    return speaker_multiple


def load_conversation_train(speaker_multiple):
    r"""loading corresponding conversation recordings into the train set
    Returns
    -------
    None
    """
    directory = parent_path + "/audio"
    directory += "/train"
    print ("\nloading conversation recordings into {}".format(directory))
    counter = 0
    for file in dir_list_c:
        speaker_id = re.split('_',file)[0]
        if speaker_id in train_ids_c:
            counter += 1
            if not os.path.exists(directory + "/" + speaker_id[2:]):
                os.makedirs(directory + "/" + speaker_id[2:])
            src = audio_path_c + "/" + file
            dst = directory + "/" + speaker_id[2:] + "/" + file
            if speaker_id[2:] in speaker_multiple:
                print (" {} has multiple recordings under its name".format(speaker_id))
                pre = re.split("_",file)[0][:2]
                end = re.split("_",file)[1].split(".")[0]
                newfile = re.split("_",file)[0][2:] + '_' + pre + end + ".flac"
                newname = directory + "/" + speaker_id[2:] + "/" + newfile
                print ("formated it from {} to {}".format(file, newname))
            else: 
                newname = directory + "/" + speaker_id[2:] + "/" + file[2:]
            copyfile(src, dst)
            os.rename(dst, newname)
    assert (counter == 83), "should move 83 files from conversation to the train folder, the number mismatched, investigate"
    print ("loading finished")
    print ("loaded {} conversation recordings in to train set ".format(counter))

print("\n(ง'̀-'́)ง you are executing audio_data_prep.py\n")

parent_path = os.path.split(os.getcwd())[0]
print ("the parent path is {}".format(parent_path))

audio_path_i = parent_path + '/LDC2015S04/seame_d2/data/interview/audio'
audio_path_c = parent_path + '/LDC2015S04/seame_d1/data/conversation/audio'

dir_list_i = get_file_list(audio_path_i, 'interview')
dir_list_c = get_file_list(audio_path_c, 'conversation')

id_dic_i = speaker_re_counts(dir_list_i)
id_dic_c = speaker_re_counts(dir_list_c)

test_short_ids_i = ['01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB']
test_short_ids_c = ['01NC01FB', '01NC02FB','06NC11MA', '06NC12MA']

train_ids_i, test_ids_i = train_test_split(id_dic_i, test_short_ids_i, "interview")
train_ids_c, test_ids_c = train_test_split(id_dic_c, test_short_ids_c, "conversation")

test_wannabe_i = create_test_wannabe(dir_list_i, test_ids_i, "interview")
test_wannabe_c = create_test_wannabe(dir_list_c, test_ids_c, "conversation")

directory = parent_path+"/audio/test"
if os.path.exists(directory):
    clean_up(directory) # remove whatever is already in the test directory
    
load_audios_to_test(test_wannabe_i, audio_path_i, "interview")

load_audios_to_test(test_wannabe_c, audio_path_c, "conversation")

load_interview_train(dir_list_i) 

speaker_multiple = get_speaker_multiple(train_ids_c)
load_conversation_train(speaker_multiple)


print("\n(ง'̀-'́)ง audio data is successfully prepared!")


