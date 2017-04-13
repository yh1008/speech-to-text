#!/usr/bin/python3

__author__="Emily Hua"

"""
This built text and segments files using filtered transcripts
"""

import os
import re
import sys
from collections import defaultdict 
parent_path = os.path.split(os.getcwd())[0]

# In kaldi/egs/code-switch directory, create a folder **data**. Then create **test** and **train** subfolders inside. Create in each subfolder following files (so you have files named in the same way in test and train subfolders but they relate to two different data sets that you created before):


directory = parent_path + "/data/train"
if not os.path.exists(directory):
    os.makedirs(directory)


directory = parent_path + "/data/test"
if not os.path.exists(directory):
    os.makedirs(directory)

# a.) spk2gender 
# This file informs about speakers gender. As we assumed, 'speakerID' is a unique name of each speaker.

# Pattern: [speakerID] [gender]

def count_files(audio_path):
    dir_list = os.listdir(audio_path)[1:]
    print ("there are total {} of files in {}\n".format(len(dir_list), audio_path))
    return dir_list
audio_path_i = parent_path + '/LDC2015S04/seame_d2/data/interview/audio'
audio_path_c = parent_path + '/LDC2015S04/seame_d1/data/conversation/audio'
dir_list_i = count_files(audio_path_i)
dir_list_c = count_files(audio_path_c)


def speaker_re_counts(dir_list):
    id_dic = defaultdict(int)
    for file in dir_list:
        id_dic[re.split('_', file)[0]] += 1
    print ('there are {} unique prefix sets'.format(len(id_dic)))
    return id_dic
id_dic_i = speaker_re_counts(dir_list_i)
id_dic_c = speaker_re_counts(dir_list_c)

test_short_ids_i = ['01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB']
test_short_ids_c = ['01NC01FB', '01NC02FB','06NC11MA', '06NC12MA']

def train_test_split(id_dic, test_short_ids):
    train_ids = []
    test_ids = []
    for key in id_dic:
        if key[2:-1] in test_short_ids or key[:-1] in test_short_ids:
            test_ids.append(key)
        else: 
            train_ids.append(key)
    print ('there are {} speaker ids in the training set'.format(len(train_ids)))
    print ('there are {} speaker ids in the testing set\n'.format(len(test_ids)))
    return train_ids, test_ids
train_ids_i, test_ids_i = train_test_split(id_dic_i, test_short_ids_i)
train_ids_c, test_ids_c = train_test_split(id_dic_c, test_short_ids_c)

print ("parent path: {}".format(parent_path))


# add interview speaker id to the train 
directory = parent_path + "/data/train/spk2gender"
with open(directory, 'w') as outfile:
    for speakerid in train_ids_i:
        outfile.write("{} {}\n".format(speakerid,speakerid[4].lower()))


# add conversation speaker id to the train 
directory = parent_path + "/data/train/spk2gender"
with open(directory, 'a+') as outfile:
    for speakerid in train_ids_c:
        if speakerid == ".DS":
            continue
        else:
            if speakerid[2:] == "NC50XFB":
                gender = 'f'            
            else:
                #print(speakerid)
                gender = speakerid[6]
        outfile.write("{} {}\n".format(speakerid[2:], gender.lower()))

# add interview speaker id to the test 
directory = parent_path + "/data/test/spk2gender"
with open(directory, 'w') as outfile:
    for speakerid in test_ids_i:
        outfile.write("{} {}\n".format(speakerid, speakerid[4].lower()))


# add conversation speaker id to the test 
directory = parent_path + "/data/test/spk2gender"
with open(directory, 'a+') as outfile:
    for speakerid in test_ids_c:
        outfile.write("{} {}\n".format(speakerid[2:], speakerid[6].lower()))
        
print ("finish creating spk2gender in train and test set ")



# b.) wav.scp 
# This file connects every utterance (sentence said by one person during particular recording session) with an audio file related to this utterance. If you stick to my naming approach, 'utteranceID' is nothing more than 'speakerID' (speaker's folder name) glued with *.wav file name without '.wav' ending (look for examples below).

# Pattern: [recordingID] [full_path_to_audio_file]

# add interview train into wav.scp 

directory = parent_path + "/data/train/wav.scp"
with open(directory, 'w') as outfile:
    for file in dir_list_i:
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids_i:
            path = parent_path + "/audio/train/" + speaker_id + "/" + file
            outfile.write("{} flac -c -d -s {} |\n".format(re.split("\.", file)[0], path))
        


# need to carefully re-name recordings in conversation, cause they don't have the speaker id as prefix. In their original naming convension, recordings from the same speaker will be identifies as different speaker. 

# add conversation train into wav.scp 
speaker_multiple = ['NC50FBP', 'NC44MBQ', 'NC45MBP', 'NC05FAX', 'NC49FBQ', 'NC41MBP', 'NC07FBX', 'NC03FBX', 'NC04FBY', 'NC10MAY', 'NC37MBP', 'NC36MBQ', 'NC35FBQ', 'NC22MBQ', 'NC08FBY', 'NC48FBP', 'NC06FAY', 'NC43FBQ', 'NC09FAX']
directory = parent_path + "/data/train/wav.scp"
with open(directory, 'a+') as outfile:
    for file in dir_list_c:
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids_c:
            if speaker_id[2:] in speaker_multiple:
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
            

# add interview test into wav.scp 

directory = parent_path + "/data/test/wav.scp"
with open(directory, 'w') as outfile:
    for file in dir_list_i:
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids_i:
            path = parent_path + "/audio/test/" + speaker_id + "/" + file
            outfile.write("{} flac -c -d -s {} |\n".format(re.split("\.", file)[0], path))

# add conversation test into wav.scp 

directory = parent_path + "/data/test/wav.scp"
with open(directory, 'a+') as outfile:
    for file in dir_list_c:
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids_c:
            path = parent_path + "/audio/test/" + speaker_id[2:] + "/" + file[2:]
            outfile.write("{} flac -c -d -s {} |\n".format(re.split("\.", file)[0][2:], path))
print ("finish creating wav.scp in train and test set")



# c.) text 
# This file contains every utterance matched with its text transcription.
# Pattern: [uterranceID] [text_transcription]

trans_path_i = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript_filtered"
trans_list_i = os.listdir(trans_path_i)[1:]
trans_path_c = parent_path + "/LDC2015S04/seame_d1/data/conversation/transcript_filtered"
trans_list_c = os.listdir(trans_path_c)[1:]

directory = parent_path + "/data/train/text"
with open(directory, 'w') as outputfile:
    for file in trans_list_i: 
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids_i:
            trans_file = trans_path_i + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    text = " ".join(re.split(" ", line)[3:])
                    #text = re.split(" ", line)[-1]
                    prefix = re.split(" ", line)[0]
                    first_frame = re.split(" ", line)[1].zfill(7)
                    second_frame = re.split(" ", line)[2].zfill(7)
                    utterance_id = prefix + "_" + first_frame + "_" + second_frame
                    outputfile.write("{} {}".format(utterance_id, text))

# create conversation text in train set 
speaker_multiple = ['NC50FBP', 'NC44MBQ', 'NC45MBP', 'NC05FAX', 'NC49FBQ', 'NC41MBP', 'NC07FBX', 'NC03FBX', 'NC04FBY', 'NC10MAY', 'NC37MBP', 'NC36MBQ', 'NC35FBQ', 'NC22MBQ', 'NC08FBY', 'NC48FBP', 'NC06FAY', 'NC43FBQ', 'NC09FAX']
directory = parent_path + "/data/train/text"
counter = 0 
with open(directory, 'a+') as outputfile:
    for file in trans_list_c: 
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids_c:
            trans_file = trans_path_c + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    if speaker_id[2:] in speaker_multiple:
                        pre = re.split("_",file)[0][:2]
                        end = re.split("_",file)[1].split(".")[0]
                        prefix = re.split("_",file)[0][2:] + '_' + pre + end
                        #print ("this speaker {} has multiple recordings, renaming it to {}".format(speaker_id, prefix))

                    else: 
                        prefix = re.split(" ", line)[0][2:]
                    text = " ".join(re.split(" ", line)[3:])
                    first_frame = re.split(" ", line)[1].zfill(7)
                    second_frame = re.split(" ", line)[2].zfill(7)
                    utterance_id = prefix + "_" + first_frame + "_" + second_frame
                    outputfile.write("{} {}".format(utterance_id, text))


directory = parent_path + "/data/test/text"
with open(directory, 'w') as outputfile:
    for file in trans_list_i: 
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids_i:
            trans_file = trans_path_i + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    text = " ".join(re.split(" ", line)[3:])
                    prefix = re.split(" ", line)[0]
                    first_frame = re.split(" ", line)[1].zfill(7)
                    second_frame = re.split(" ", line)[2].zfill(7)
                    utterance_id = prefix + "_" + first_frame + "_" + second_frame
                    outputfile.write("{} {}".format(utterance_id, text))

# create conversation text in test 
directory = parent_path + "/data/test/text"
with open(directory, 'a+') as outputfile:
    for file in trans_list_c: 
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids_c:
            trans_file = trans_path_c + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    text = " ".join(re.split(" ", line)[3:])
                    prefix = re.split(" ", line)[0][2:]
                    first_frame = re.split(" ", line)[1].zfill(7)
                    second_frame = re.split(" ", line)[2].zfill(7)
                    utterance_id = prefix + "_" + first_frame + "_" + second_frame
                    outputfile.write("{} {}".format(utterance_id, text))
                    
print ("finish create text in train and test set")


# d.) utt2spk 
# This file tells the ASR system which utterance belongs to particular speaker.
# Pattern: [uterranceID] [speakerID]

trans_list = os.listdir(trans_path_i)[1:]
largest_frame = -sys.maxsize
trans_list_i = os.listdir(trans_path_i)[1:]
print ("there are {} recording with transcript".format(len(trans_list_i)))
print ("there are {} recording in audio files".format(len(dir_list_i)))

for file in trans_list_i:
    file_path = trans_path_i + "/" + file
    if file == ".DS_Store":
        continue
    else:
        with open(file_path, 'r') as inputfile:
            for line in inputfile:
                #print(line)
                second_frame = int(re.split(" ", line)[2])
                if second_frame > largest_frame:
                    largest_frame = second_frame
print ("largest_frame is {}".format(largest_frame))  


for file in trans_list_c:
    file_path = trans_path_c + "/" + file
    if file == ".DS_Store":
        continue
    else:
        with open(file_path, 'r') as inputfile:
            for line in inputfile:
                second_frame = int(re.split(" ", line)[2])
                if second_frame > largest_frame:
                    largest_frame = second_frame
print ("largest_frame is {}".format(largest_frame))  
print ("since 7242490 is our largest frame, then we need to create string with 7 digits to hold all frames")

# create utterance id for interview: recording id + start time + end time; for e.g. NI01MAX_0101_0001353_0003612
counter = 0
utter_ids_i = []
for file in trans_list_i:
    file_path = trans_path_i + "/" + file
    if file == ".DS_Store":
        continue
    else:
        with open(file_path, 'r') as inputfile:
            for line in inputfile:
                speaker_id = re.split("_", line)[0]
                prefix = re.split(" ", line)[0]
                first_frame = re.split(" ", line)[1].zfill(7)
                second_frame = re.split(" ", line)[2].zfill(7)
                utterance_id =  prefix + "_" + first_frame + "_" + second_frame
                utter_ids_i.append(utterance_id)
print ("there are {} new utterance ids".format(len(utter_ids_i)))



# create utterance id for conversation
counter = 0
utter_ids_c = []
for file in trans_list_c:
    file_path = trans_path_c + "/" + file
    if file == ".DS_Store":
        continue
    else:
        with open(file_path, 'r') as inputfile:
            for line in inputfile:
                speaker_id = re.split("_", line)[0]
                if speaker_id[2:] in speaker_multiple:
                    pre = re.split("_",file)[0][:2]
                    end = re.split("_",file)[1].split(".")[0]
                    prefix = re.split("_",file)[0][2:] + '_' + pre + end
                else:
                    prefix = re.split(" ", line)[0][2:]
                first_frame = re.split(" ", line)[1].zfill(7)
                second_frame = re.split(" ", line)[2].zfill(7)
                utterance_id =  prefix + "_" + first_frame + "_" + second_frame
                utter_ids_c.append(utterance_id)
print ("there are {} new utterance ids".format(len(utter_ids_c)))
print("sample newly created utterance id {}".format(utter_ids_i[:1]))
print("sample newly created utterance id {}".format(utter_ids_c[:1]))

train_ids_c_short = [ x[2:] for x in train_ids_c]

utt2spk_path = parent_path + "/data/train/utt2spk"
counter = 0
with open(utt2spk_path, 'w') as outputfile:
    for file in utter_ids_i:
        speaker_id = re.split("_", file)[0]
        if speaker_id in train_ids_i:
            counter += 1
            outputfile.write("{} {}\n".format(file, speaker_id))
    for file in utter_ids_c:
        speaker_id = re.split("_",file)[0]
        if speaker_id in train_ids_c_short:
            counter += 1
            outputfile.write("{} {}\n".format(file, speaker_id))
print ("there are {} in train/utt2spk".format(counter))


test_ids_c_short = [x[2:] for x in test_ids_c]
utt2spk_path = parent_path + "/data/test/utt2spk"
counter = 0
with open(utt2spk_path, 'w') as outputfile:
    for file in utter_ids_i:
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids_i:
            counter += 1
            outputfile.write("{} {}\n".format(file, speaker_id))
    for file in utter_ids_c:
        speaker_id = re.split("_", file)[0]
        if speaker_id in test_ids_c_short:
            counter += 1
            outputfile.write("{} {}\n".format(file, speaker_id))
print ("there are {} in test/utt2spk".format(counter))



# e.) corpus.txt 
# Pattern: [text_transcription]

temp_path = parent_path + "/data/local"
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
    
corpus_path = parent_path + "/data/local/corpus.txt"
trans_path = parent_path + "/LDC2015S04/seame_d2/data/interview/transcript_filtered"
trans_list = os.listdir(trans_path)[1:]

with open(corpus_path, 'w') as outputfile:
    for file in trans_list: 
            trans_file = trans_path + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    #outputfile.write(line)
                    outputfile.write(" ".join(re.split(" ", line)[3:]))


temp_path = parent_path + "/data/local"
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
    
corpus_path = parent_path + "/data/local/corpus.txt"
trans_path = parent_path + "/LDC2015S04/seame_d1/data/conversation/transcript_filtered"
trans_list = os.listdir(trans_path)[1:]

with open(corpus_path, 'a+') as outputfile:
    for file in trans_list: 
            trans_file = trans_path + "/" + file
            with open(trans_file, 'r') as inputfile:
                for line in inputfile:
                    outputfile.write(" ".join(re.split(" ", line)[3:]))


# (f) segments file  
# the format of the "segments" file is:  
# [utterance-id] [recoding-id] [segment-begin] [segment-end]   

# (interview) segments file for training set
directory = parent_path + "/data/train/segments"
counter = 0
with open(directory, 'w') as outputfile:
    for utt in utter_ids_i:
        speaker_id = re.split("_", utt)[0]
        if speaker_id in train_ids_i:
            
            recording_id = "_".join(utt.split("_", 2)[:2])
            segment_begin = str(int(re.split("_", utt)[2])/1000.0)
            segment_end = str(int(re.split("_", utt)[3])/1000.0)
            outputfile.write("{} {} {} {}\n".format(utt, recording_id, segment_begin, segment_end))
    
       

# (conversation) segments file for training set
directory = parent_path + "/data/train/segments"
counter = 0
with open(directory, 'a+') as outputfile:
    for utt in utter_ids_c:
        speaker_id = re.split("_", utt)[0]
        if speaker_id in train_ids_c_short:          
            recording_id = "_".join(utt.split("_", 2)[:2])
            segment_begin = str(int(re.split("_", utt)[2])/1000.0)
            segment_end = str(int(re.split("_", utt)[3])/1000.0)
            outputfile.write("{} {} {} {}\n".format(utt, recording_id, segment_begin, segment_end))


# (interview) create segments file for training set
directory = parent_path + "/data/test/segments"
counter = 0 
with open(directory, 'w') as outputfile:
    for utt in utter_ids_i:
        speaker_id = re.split("_", utt)[0]
        if speaker_id in test_ids_i:
            recording_id = "_".join(utt.split("_", 2)[:2])
            segment_begin = str(int(re.split("_", utt)[2])/1000.0)
            segment_end = str(int(re.split("_", utt)[3])/1000.0)
            outputfile.write("{} {} {} {}\n".format(utt, recording_id, segment_begin, segment_end))
            counter += 1

# (conversation) create conversation segments file for test set
directory = parent_path + "/data/test/segments"
counter = 0 
with open(directory, 'a+') as outputfile:
    for utt in utter_ids_c:
        speaker_id = re.split("_", utt)[0]
        if speaker_id in test_ids_c_short:
            recording_id = "_".join(utt.split("_", 2)[:2])
            segment_begin = str(int(re.split("_", utt)[2])/1000.0)
            segment_end = str(int(re.split("_", utt)[3])/1000.0)
            outputfile.write("{} {} {} {}\n".format(utt, recording_id, segment_begin, segment_end))
            counter += 1
            
print ("Wow, the acoustic data is successfully prepared") 
