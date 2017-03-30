#!/usr/bin/python3


__author__="Emily Hua"


# Go to kaldi/egs/code-switch directory and create itnerview_audio folder. In kaldi-trunk/egs/code-switch/interview_audio create two folders: train and test. Select ten speaker of your choice to represent testing data set. Use this speaker's 'speakerID' as a name for an another new folder in kaldi-trunk/egs/code-switch/interview_audio/test directory. Then put there all the audio files related to that person. Put the rest (84 speakers) into train folder - this will be your training data set. Also create subfolders for each speaker.



import os
parent_path = os.path.split(os.getcwd())[0]
print (parent_path)


# In[5]:

def count_files(audio_path):
    dir_list = os.listdir(audio_path)[1:]
    print ("there are total {} of files in {}\n".format(len(dir_list), audio_path))
    return dir_list
audio_path_i = parent_path + '/LDC2015S04/seame_d2/data/interview/audio'
audio_path_c = parent_path + '/LDC2015S04/seame_d1/data/conversation/audio'
dir_list_i = count_files(audio_path_i)
dir_list_c = count_files(audio_path_c)


# In[6]:

import re
from collections import defaultdict 
def speaker_re_counts(dir_list):
    id_dic = defaultdict(int)
    for file in dir_list:
        id_dic[re.split('_', file)[0]] += 1
    print ('there are {} unique prefix sets'.format(len(id_dic)))
    return id_dic
id_dic_i = speaker_re_counts(dir_list_i)
id_dic_c = speaker_re_counts(dir_list_c)
    


# In[9]:

id_dic_cc = defaultdict(int)
for file in dir_list_c:
    id_dic_cc[re.split('_', file)[0][2:]] += 1
print ('there are {} unique prefix sets'.format(len(id_dic_cc)))


# In[28]:

print ("example speaker ids and number of recordings in converstaion they have: {}".format(dict(list(id_dic_c.items())[:3])))


# In[29]:

print ("example speaker ids and number of recordings in interview they have: {}".format(dict(list(id_dic_i.items())[:3])))


# In[12]:

test_short_ids_i = ['01MA', '03FA','08MA', '29FA','29MB','42FB','44MB','45FB','67MB','55FB']


# In[11]:

test_short_ids_c = ['01NC01FB', '01NC02FB','06NC11MA', '06NC12MA']







# In[13]:

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


# there are 85 speaker ids in the training set
# there are 10 speaker ids in the testing set
# 
# there are 75 speaker ids in the training set
# there are 4 speaker ids in the testing set

# In[14]:

print ("speaker ids in the converation test set: {}\n".format(test_ids_c))
print ("speaker ids in the interview test set: {}".format(test_ids_i))


# In[15]:

print ("speaker ids in the conversation train set: \n{}\n".format(train_ids_c))
print ("speaker ids in the interview train set: \n{}".format(train_ids_i))


# In[16]:

def create_test_wannabe(dir_list, test_ids):
    test_wannabe = []
    for file in dir_list:
        speaker_id = re.split('_', file)[0]
        if speaker_id in test_ids:
            test_wannabe.append(file)
            # I have add a file from this prefix into the test set, no need for more from this prefix
    print ("there are {} files ready to be moved into the test set".format(len(test_wannabe)))    
    return test_wannabe
test_wannabe_i = create_test_wannabe(dir_list_i, test_ids_i)
test_wannabe_c = create_test_wannabe(dir_list_c, test_ids_c)


# should be   
# there are 16 files ready to be moved into the test set  
# there are 4 files ready to be moved into the test set  
# 


# load interview recordings into the test set 
from shutil import copyfile
directory = parent_path + "/audio"
if not os.path.exists(directory):
    os.makedirs(directory)
print (directory)
directory += "/test"
print ("loading interview recordings into {}".format(directory))
if not os.path.exists(directory):
    os.makedirs(directory)
    for file in test_wannabe_i:
        speaker_id = re.split('_',file)[0]
        if not os.path.exists(directory + "/" + speaker_id):
            os.makedirs(directory + "/" + speaker_id)
        src = audio_path_i + "/" + file
        dst = directory + "/" + speaker_id + "/" + file
        copyfile(src, dst)
print ("loading finished")




# load conversation recordings into the test set
from shutil import copyfile
directory = parent_path + "/audio"
if not os.path.exists(directory):
    os.makedirs(directory)
print (directory)
directory += "/test"
print ("loading conversation recordings into {}".format(directory))

for file in test_wannabe_c:
    speaker_id = re.split('_',file)[0][2:]
    if not os.path.exists(directory + "/" + speaker_id):
        os.makedirs(directory + "/" + speaker_id)
    src = audio_path_c + "/" + file
    dst = directory + "/" + speaker_id + "/" + file
    newname = directory + "/" + speaker_id + "/" + file[2:]
    copyfile(src, dst)
    os.rename(dst, newname)
print ("loading finished")



# In[26]:

# loading interview recordings into the train set 
from shutil import copyfile
directory = parent_path + "/audio"
directory += "/train"
print ("loading interview recordings into {}".format(directory))
if not os.path.exists(directory):
    os.makedirs(directory)
    for file in dir_list_i:
        speaker_id = re.split('_',file)[0]
        if speaker_id in train_ids_i:
            if not os.path.exists(directory + "/" + speaker_id):
                os.makedirs(directory + "/" + speaker_id)
            src = audio_path_i + "/" + file
            dst = directory + "/" + speaker_id + "/" + file
            copyfile(src, dst)
print ("loading finished")




# In[29]:

# find me conversation with different recordings under the same speaker 
train = ['15NC29FBP', '29NC53MBP', '28NC52FBQ', '20NC39MBP', '04NC08FBY', '10NC20MBQ', '19NC37MBP', '40NC58FAY', '23NC45MBP', '46NC41MBP', '07NC14FBQ', '32NC36MBQ', '12NC24FBQ', '34NC37MBP', '13NC25MBP', '28NC51MBP', '31NC35FBQ', '25NC43FBQ', '26NC49FBQ', '31NC50XFB', '14NC28MBQ', '44NC44MBQ', '03NC06FAY', '33NC43FBQ', '09NC17FBP', '04NC07FBX', '45NC22MBQ', '26NC48FBP', '37NC45MBP', '27NC47MBQ', '18NC36MBQ', '15NC30MBQ', '02NC03FBX', '05NC10MAY', '03NC05FAX', '32NC50FBP', '36NC46FBQ', '11NC21FBP', '35NC56MBP', '11NC22MBQ', '19NC38FBQ', '22NC43FBP', '12NC23FBP', '29NC54FBQ', '07NC13MBP', '39NC57FBX', '25NC47MBP', '08NC16FBQ', '22NC44MBQ', '21NC41MBP', '17NC33FBP', '16NC31FBP', '08NC15MBP', '18NC35FBP', '05NC09FAX', '09NC18MBQ', '14NC27MBP', '42NC60FBQ', '17NC34FBQ', '30NC48FBP', '10NC19MBP', '41NC59MAX', '24NC35FBQ', '43NC61FBQ', '24NC45MBP', '27NC50FBP', '13NC26MBQ', '33NC37MBP', '30NC49FBQ', '16NC32FBQ', '02NC04FBY', '20NC40FBQ', '38NC50FBP', '23NC35FBQ', '21NC42MBQ']
speaker_multiple = []
sets = set([])
for i in train:
    sets.add(i[2:])
print (len(sets))
print (len(train))

dic = defaultdict(list)
for file in dir_list_c:
    dic[re.split("_",file)[0][2:]].append(file)

for key in dic:
    if len(dic[key]) > 1 :
        speaker_multiple.append(key)
print ("speakers with multiple recordings:\n {}".format(speaker_multiple))


# In[30]:

# loading conversation recordings into the train set 
from shutil import copyfile
directory = parent_path + "/audio"
directory += "/train"
print ("loading conversation recordings into {}".format(directory))
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
        
print ("loading finished")
print ("loaded {} conversation recordings in to train set ".format(counter))





