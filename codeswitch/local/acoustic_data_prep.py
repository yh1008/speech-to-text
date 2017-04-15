#!/usr/bin/env python3
# coding: utf-8
__author__="Emily Hua"

"""This is the main module that structures the acoustic files for Kaldi to consume
The following six files will be created upon execution:
    (spk2gender, utt2spk, wav.scp, text, corpus, segments),
where text and segments files are built using filtered transcripts
"""

import os
import re
import sys
import glob
from shutil import rmtree
from collections import defaultdict 


def makedir(dirt):
    r"""create data/train or data/test directory
    """
    directory = parent_path + "/data/" + dirt
    if not os.path.exists(directory):
        os.makedirs(directory)


# a.) spk2gender 

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



def generate_spk2gender(id_list, dirt, dirn):
    r"""create spk2gender file under data/train or data/test
    Returns
    -------
    None
    """
    if dirt == "train":
        directory = parent_path + "/data/train/spk2gender"
    elif dirt == "test":
        directory = parent_path + "/data/test/spk2gender"
    with open(directory, 'a+') as outfile:
        for speakerid in id_list:
            if dirn == "conversation":
                speakerid = speakerid[2:]
                if speakerid == "NC50XFB": # this speaker is originally gender unknown, to prevent it from being filtered out by Kaldi, I assign it to be female
                    gender = 'f'
            gender = speakerid[4].lower()
            outfile.write("{} {}\n".format(speakerid, gender))


def dir_clean_up(dir_path):
    files = glob.glob(dir_path + '/*')
    for f in files:
        rmtree(f)


def file_clean_up(dir_path, fn):
    to_be_removed = dir_path + "/" + fn
    if os.path.isfile(to_be_removed):
        os.remove(to_be_removed)


# b.) wav.scp 
def generate_wavscp(dir_list, id_list, dirt, dirn):
    r"""generate wav.scp in data/train or data/test 
    the pattern for each line of the wav.scp file is <recording_id><full_path_to_audio_file> 
    because our audio is in flac, I need to tell Kaldi to convert it at some time
    e.g. NC07FBX_040201 flac -c -d -s /codeswitch/audio/train/NC07FBX/NC07FBX_040201.flac |
    Returns
    -------
    None 
    """
    if dirt == "train":
        directory = parent_path + "/data/train/wav.scp"
    else:
        directory = parent_path + "/data/test/wav.scp"
    with open(directory, 'a+') as outfile:
        counter = 0
        for file in dir_list:
            speaker_id = re.split("_", file)[0]
            if dirt == "train" and dirn == "conversation":
                if speaker_id in id_list:
                    counter += 1
                    if speaker_id[2:] in speaker_multiple: # rename e.g. 04NC07FBX_0201.flac to NC07FBX_040201.flac
                        pre = re.split("_",file)[0][:2]
                        end = re.split("_",file)[1].split(".")[0]
                        newfile = re.split("_",file)[0][2:] + '_' + pre + end + ".flac"
                        path = parent_path + "/audio/train/" + speaker_id[2:] + "/" + newfile
                        recording_id = re.split("\.", newfile)[0]
                        #print ("this {} has multiple recordings, renaming them to {}".format(speaker_id, newfile))
                    else: 
                        path = parent_path + "/audio/train/" + speaker_id[2:] + "/" + file[2:]
                        recording_id = re.split("\.", file)[0][2:]
                    
                    outfile.write("{} flac -c -d -s {} |\n".format(recording_id, path))

            else: 
                if dirn == "interview" and speaker_id in id_list and dirt =="train":
                    counter += 1
                    recording_id = re.split("\.", file)[0]
                    path = parent_path + "/audio/train/" + speaker_id + "/" + file
                    outfile.write("{} flac -c -d -s {} |\n".format(recording_id, path))
                elif dirn == "interview" and speaker_id in id_list and dirt == "test":
                    counter += 1
                    recording_id = re.split("\.", file)[0]
                    path = parent_path + "/audio/test/" + speaker_id + "/" + file
                    outfile.write("{} flac -c -d -s {} |\n".format(recording_id, path))
                elif dirn == "conversation" and speaker_id in id_list and dirt == "test":
                    counter += 1
                    recording_id = re.split("\.", file)[0][2:]
                    path = parent_path + "/audio/test/" + speaker_id[2:] + "/" + file[2:]
                    outfile.write("{} flac -c -d -s {} |\n".format(recording_id, path))
                    
        if dirt == "train" and dirn == "conversation":
            assert(counter == 83), "should write 83 lines from conversation to wav.scp (train)"
        elif dirt == "test" and dirn == "conversation":
            assert(counter == 4), "should write 4 lines from conversation to wav.scp (test)"
        elif dirt == "train" and dirn == "interview":
             assert(counter == 194), "should write 194 lines from interview to wav.scp (train)"
        else:
            assert(counter == 16), "should write 16 lines from interview to wav.scp (test)"


# c.) text 
def write_text(file_list, trans_path, id_list, dirt, dirn):
    r"""generate text file
    for each line the pattern is: <utterance_id><transcript>
    e.g. NC03FBX_0101_0008400_0010710 就 那种 TYPICAL 的 偶 像 剧
    """
    if dirt == "test":
        directory = parent_path + "/data/test/text"
    elif dirt == "train":
        directory = parent_path + "/data/train/text"
    counter = 0
    with open(directory, 'a+') as outputfile:
        for file in file_list:
            speaker_id = re.split("_", file)[0]
            if speaker_id in id_list: 
                trans_file = trans_path + "/" + file
                with open(trans_file, 'r') as inputfile: # only read file from transcript_filtered if the speaker is a match
                    for line in inputfile:
                        if dirn =="conversation" and dirt == "train":
                            if speaker_id[2:] in speaker_multiple:
                                pre = re.split("_",file)[0][:2] # e.g. 04
                                end = re.split("_",file)[1].split(".")[0] # e.g. 0201
                                prefix = re.split("_",file)[0][2:] + '_' + pre + end  #make 04NC08FBY_0201 -> NC08FBY_040201
                            else:
                                prefix = re.split(" ", line)[0][2:] #make prefix 02NC03FBX_0101 -> NC03FBX_0101
                            
                        elif dirn =="conversation" and dirt == "test":
                            prefix = re.split(" ", line)[0][2:]
                        else:
                            prefix = re.split(" ", line)[0]
                        text = " ".join(re.split(" ", line)[3:])
                        first_frame = re.split(" ", line)[1].zfill(7)
                        second_frame = re.split(" ", line)[2].zfill(7)
                        utterance_id = prefix + "_" + first_frame + "_" + second_frame
                        outputfile.write("{} {}".format(utterance_id, text))
                        counter += 1
        print ("write {} lines of {} text from {}".format(counter, dirt, dirn))
        if dirt == "train" and dirn == "conversation":
            pass
            #assert(counter == 13731), "should write 13731 lines from conversation to text (train)"
        elif dirt == "test" and dirn == "conversation":
            pass
            #assert(counter == 485, "should write 485 lines from conversation to text(test)"
        elif dirt == "train" and dirn == "interview":
            pass
            #assert(counter == 29505), "should write 29505 lines from interview to text (train)"
        else:
            pass
            #assert(counter == 2909), "should write 2909 lines from interview to wav.scp (test)" 


# d.) utt2spk 
def get_largest_frame(trans_list, trans_path):
    largest_frame = -sys.maxsize
    for file in trans_list:
        file_path = trans_path + "/" + file
        with open(file_path, 'r') as inputfile:
            for line in inputfile:
                second_frame = int(re.split(" ", line)[2])
                if second_frame > largest_frame:
                    largest_frame = second_frame
    return largest_frame

def get_frame_size(frame1, frame2):
    gframe = frame1
    if gframe < frame2:
        gframe = frame2
    size = len(list(str(gframe)))
    print ("since {} is our largest frame, then we need to create string with {} digits to hold all frames\n".format(gframe, size))
    return size

def gen_utter_list(trans_list, trans_path, dirn):
    r"""create a list of utterance_id
    e.g. ['UI29FAZ_0104_0985128_0986293']
    Returns
    -------
    utter_ids : list
        A list of utterance_id
    """
    utter_ids = []
    for file in trans_list:
        file_path = trans_path + "/" + file
        with open(file_path, 'r') as inputfile:
            for line in inputfile:
                speaker_id = re.split("_", line)[0]
                if dirn == "conversation":
                    if speaker_id[2:] in speaker_multiple:
                        pre = re.split("_",file)[0][:2]
                        end = re.split("_",file)[1].split(".")[0]
                        prefix = re.split("_",file)[0][2:] + '_' + pre + end
                    else:
                        prefix = re.split(" ", line)[0][2:]
                else:
                    prefix = re.split(" ", line)[0]
                first_frame = re.split(" ", line)[1].zfill(7)
                second_frame = re.split(" ", line)[2].zfill(7)
                utterance_id =  prefix + "_" + first_frame + "_" + second_frame
                utter_ids.append(utterance_id)
    print ("{} has {} utterance ids in total".format(dirn, len(utter_ids)))
    return utter_ids


def create_utt2spk(id_list, utter_ids, dirt, dirn):
    r"""create utt2spk file in data/train or data/test
    For each line of utt2spk file the pattern is <utterance_id><speaker_id>
    e.g. NC01FBX_0101_0086300_0088370 NC01FBX
    Returns
    -------
    None
    """
    counter = 0
    if dirt == "train":
        utt2spk_path = parent_path + "/data/train/utt2spk"
    else:
        utt2spk_path = parent_path + "/data/test/utt2spk"
    if dirn == "conversation":
        id_list = [x[2:] for x in id_list]
    with open(utt2spk_path, 'a+') as outputfile:
        for file in utter_ids:
            speaker_id = re.split("_", file)[0]
            if speaker_id in id_list:
                counter += 1
                outputfile.write("{} {}\n".format(file, speaker_id))
    print ("write {} lines of utt2spk from {}".format(counter, dirn))


# e.) corpus.txt 
def write_corpus(trans_list, trans_path, train_ids, dirn):
    r"""write only transcript used in training to corpus.txt
    each line of the corpus.txt has pattern <text_transcription>
    e.g. 就是 那种 TYPICAL 偶 像 剧
    Returns
    -------
    None
    """
    counter = 0
    temp_path = parent_path + "/data/local"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path) 
    corpus_path = parent_path + "/data/local/corpus.txt"
    with open(corpus_path, 'a+') as outputfile:
        for file in trans_list:
            speaker_id = re.split("_",file)[0]
            if speaker_id in train_ids: # only take in training set transcript to over information leakage
                trans_file = trans_path + "/" + file
                with open(trans_file, 'r') as inputfile:
                    for line in inputfile:
                        counter += 1
                        outputfile.write(" ".join(re.split(" ", line)[3:]))
    print ("{} lines of transcript from {} is written to data/local/corpus.txt (training data only)".format(counter, dirn))


# (f) segments file  
def gen_segments(utter_ids, id_list, dirt, dirn):
    r"""create segments file under data/train or data/test
    for each line of this file has pattern <utterance_id><recording_id><segments_begin><segments_end>,
    where <segments_begin> and <segments_end> are in second
    e.g.
    Returns
    -------
    None
    """
    counter = 0
    if dirt == "train":
        directory = parent_path + "/data/train/segments"
    else:
        directory = parent_path + "/data/test/segments"
    if dirn == "conversation":
        id_list = [i[2:] for i in id_list]
    with open(directory, 'a+') as outputfile:
        for utt in utter_ids:
            speaker_id = re.split("_", utt)[0]
            if speaker_id in id_list:
                recording_id = "_".join(utt.split("_", 2)[:2])
                segment_begin = str(int(re.split("_", utt)[2])/1000.0) # make sure it doesn't get rounded by python2
                segment_end = str(int(re.split("_", utt)[3])/1000.0)
                counter += 1
                outputfile.write("{} {} {} {}\n".format(utt, recording_id, segment_begin, segment_end))
    print ("{} of lines of {} is written to segments in data/{}".format(counter, dirn, dirt))

print("\n  you are executing acoustic_data_prep.py\n")

parent_path = os.path.split(os.getcwd())[0]
print ("parent path is {}".format(parent_path))
makedir("train")
makedir("test")

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


# clean up existing spk2gender
file_clean_up(parent_path + "/data/train", "spk2gender")
file_clean_up(parent_path + "/data/test", "spk2gender")

generate_spk2gender(train_ids_i, "train", "interview")
generate_spk2gender(train_ids_c, "train", "conversation")
generate_spk2gender(test_ids_i, "test", "interview")
generate_spk2gender(test_ids_c, "test", "conversation")
print ("finish generating spk2gender!\n")

# clean up existing wav.scp 
file_clean_up(parent_path + "/data/train", "wav.scp")
file_clean_up(parent_path + "/data/test", "wav.scp")

speaker_multiple = ['NC50FBP', 'NC44MBQ', 'NC45MBP', 'NC05FAX', 'NC49FBQ', 'NC41MBP', 'NC07FBX', 'NC03FBX', 'NC04FBY', 'NC10MAY', 'NC37MBP', 'NC36MBQ', 'NC35FBQ', 'NC22MBQ', 'NC08FBY', 'NC48FBP', 'NC06FAY', 'NC43FBQ', 'NC09FAX']
generate_wavscp(dir_list_c, train_ids_c, "train", "conversation")
generate_wavscp(dir_list_i, train_ids_i, "train", "interview")
generate_wavscp(dir_list_c, test_ids_c, "test", "conversation")
generate_wavscp(dir_list_i, test_ids_i, "test", "interview")
print ("finish generating wav.scp!\n")

trans_path_i = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript_filtered"
trans_list_i = [f for f in os.listdir(trans_path_i) if f.endswith(".txt")]
trans_path_c = parent_path + "/LDC2015S04/seame_d1/data/conversation/transcript_filtered"
trans_list_c = [f for f in os.listdir(trans_path_c) if f.endswith(".txt")]
assert (len(trans_list_i) == 210), "there should be 210 files in interview/transcript_filtered, check if the directory is corrupted"
assert (len(trans_list_c) == 87), "there should be 87 files in conversation/transcript_filtered, check if the directory is corrupted"

# clean up existing wav.scp 
file_clean_up(parent_path + "/data/train", "text")
file_clean_up(parent_path + "/data/test", "text")

write_text(trans_list_c, trans_path_c, train_ids_c, "train", "conversation")
write_text(trans_list_i, trans_path_i, train_ids_i, "train", "interview")
write_text(trans_list_c, trans_path_c, test_ids_c, "test", "conversation")
write_text(trans_list_i, trans_path_i, test_ids_i, "test", "interview")
print ("finish creating text!\n")


frame1 = get_largest_frame(trans_list_c, trans_path_c)
frame2 = get_largest_frame(trans_list_i, trans_path_i)
size = get_frame_size(frame1, frame2)

utter_ids_i = gen_utter_list(trans_list_i, trans_path_i, "interview")
utter_ids_c = gen_utter_list(trans_list_c, trans_path_c, "conversation")

# clean up any exisiting utt2spk
file_clean_up(parent_path+"/data/train", 'utt2spk')
file_clean_up(parent_path+"/data/test", 'utt2spk')

create_utt2spk(train_ids_c, utter_ids_c, "train", "conversation")
create_utt2spk(train_ids_i, utter_ids_i, "train", "interview")
create_utt2spk(test_ids_c, utter_ids_c, "test", "conversation")
create_utt2spk(test_ids_i, utter_ids_i, "test", "interview")
print ("finish creating utt2spk file!\n")

# clean up any exisiting corpus.txt
file_clean_up(parent_path+"/data/local", 'corpus.txt')
file_clean_up(parent_path+"/data/local", 'corpus.txt')

write_corpus(trans_list_c, trans_path_c, train_ids_c, "conversation")
write_corpus(trans_list_i, trans_path_i, train_ids_i, "interview")
print(" finish creating data/lang/corpus.txt!\n")

# clean up any exisiting segments
file_clean_up(parent_path+"/data/train", 'segments')
file_clean_up(parent_path+"/data/test", 'segments')

gen_segments(utter_ids_c, train_ids_c, "train", "conversation")
gen_segments(utter_ids_i, train_ids_i, "train", "interview")
gen_segments(utter_ids_c, test_ids_c, "test", "conversation")
gen_segments(utter_ids_i, test_ids_i, "test", "interview")
print ("finish creating segments file!\n")

print ("\n acoustic data is succesfully prepared!" )