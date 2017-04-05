import codecs
import re
import os


#### settings ####
dirs = ['./LDC2015S04/seame_d1/data/conversation/transcript/','./LDC2015S04/seame_d2/data/interview/transcript/']
newfolder = 'fixed/'
dir_lang = './data/local/lang/'
dir_dicsource = ''

#### functions ####
# from https://segmentfault.com/q/1010000000732038
# to detect english character ONLY
def isAlpha(word):
    try:
        return word.encode('ascii').isalpha()
    except UnicodeEncodeError:
        return False
		
# from http://www.cnblogs.com/kaituorensheng/p/3554571.html
# -*- coding: cp936 -*-
def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring
	

#### read lexicons ####
filename_cmu = "cmudict-0.7b"
d_cmu = dict()
max_num = 0 # max number of (x) <-- a word with multiple pronunciations
f = open(dir_dicsource+filename_cmu,"r")
for line in f.readlines():
    if line[0:3] != ";;;":
        line = line[:-1]
        line = line.split("  ",1)
        d_cmu[line[0]] = line[1]
        if line[0][-1] == ")":
            try: 
                num_cur = int(line[0][-2])      
                if int(line[0][-2]) > max_num:
                    max_num = num_cur
            except:
                continue

print("Finish loading cmu dictionary")
print("Number of English lexicon: " + str(len(d_cmu)))

filename_th = "thchs30-lexicon.txt"
d_th = dict()
with codecs.open(dir_dicsource+filename_th, 'r', 'utf-8') as f:
    for line in f.readlines():
        line = line.split()
        d_th[line[0]] = ' '.join(line[1:])
print("Finish loading thchs30 dictionary")
print("Number of Chinese lexicon: " + str(len(d_th)))


#### waste word collection ####
# to get the full word list
words = []
for dir in dirs:
	filenames = os.listdir(dir)
	for filename in filenames:
		if filename[-4:] == ".txt":
			with codecs.open(dir+"/"+filename, 'r', 'utf-8') as f:
				for line in f.readlines():
					sentence = line.split() # 1st element -- audio file id, 2nd element -- start time, 3rd element -- end time
					words_cur = sentence[4:]   
					words += words_cur
				f.close()

print("Finish concatenating words")
print("Number of words: " + str(len(words)))
print("Number of unique words: " + str(len(set(words))))

# create a dictionary of waste words
words_waste = []
words_1 = [] # [x]
words_2 = [] # (x)
        
for word in words:
    if word[-1] == "]" or word[0] == "[":
        word = re.findall(r'''(\[.+?\])''',word)
        words_1 += word
    elif word[-1] == ")" or word[0] == "(":
        word = re.findall(r'''(\(.+?\))''',word)
        words_2 += word
        
words_waste = words_1 + words_2

d_waste = dict()
for word in words_waste:
    try:
        d_waste[word] += 1
    except:
        d_waste[word] = 1

d_waste2idx = dict()
idx = -1
for k in d_waste.keys():
    idx += 1
    d_waste2idx[k] = 'SIL' + str(idx)

d_idx2waste = {v:k for k,v in d_waste2idx.items()}

print("Finish creating waste word dictionary")
print("Number of waste word type: " + str(len(set(words_waste))))


#### fix, filter, output text transcript ####
# fix and output the transcript text going to be used
words_all = []
text_all = []
text_unparse = []

for dir in dirs:
	filenames = os.listdir(dir)
	for filename in filenames:
		if filename[-4:] == ".txt":
			with codecs.open(dir+filename, 'r', 'utf-8') as f:
				text = []

				for line in f.readlines():
					sentence_origin = line.strip()
                
					# deal with situations like 'co[mm]on' and 'co[mm]unication'
					words_mm_cur = set(re.findall(r'''o(\[.+?\])''',line))
					if len(words_mm_cur) > 0:
						sentence_origin = sentence_origin.replace('o[mm]','omm')
                
					# replace waste words with SILx; space after ] or before [ to avoid situations like co[mm]on or co[mm]unication
					words_waste_cur = set(re.findall(r'''(\[.+?\])''',line) + re.findall(r'''(\(.+?\))''',line))
					for element in words_waste_cur:
						try:
							sentence_origin = sentence_origin.replace(element,' ' + d_waste2idx[element] + ' ')
						except:
							continue
                
					# get rid of "#"
					sentence_origin = sentence_origin.replace('#',' ')
                
					# get rid of "="
					sentence_origin = sentence_origin.replace('=',' ')
                
					# deal with %word% like %chelsia%
					sentence_origin = sentence_origin.replace('%',' ')
                
					# deal with "word" like "william"
					sentence_origin = sentence_origin.replace('"',' ')
                
					# deal with pronunciation of single letter, for which the trascript is like P. S., I. T., etc.
					sentence_origin = sentence_origin.replace('.',' ')
                
					# Q2B
					sentence_chars = list(sentence_origin)
					for char_idx in range(len(sentence_chars)):
						sentence_chars[char_idx] = strQ2B(sentence_chars[char_idx])
					sentence_origin = "".join(sentence_chars)
                
					# trim again incase the substitution brings in space
					sentence_origin = sentence_origin.strip()
                              
					sentence = sentence_origin.split() # 1st element -- audio file id, 2nd element -- start time, 3rd element -- end time
					info_cur = sentence[:3] # idx: 0~2
					words_cur = sentence[3:] # idx: 3~
					unparse = False
    
					for word in words_cur: # filter out concatenated characters having Chinese characters, with length over 4
          
						# filter out unsegmented element (unparse = F -> unparse = T)
						# for example, [leh]每次上学的时候daddy都会买糕点给我吃买马来糕#kuih# (idx: 53628)
						try:
							d_cmu[word.upper()] # if the word is a recorded English word
							continue
						except:
							try:
								d_idx2waste[word] # if the word is SILx
								continue
							except:
								try:
									d_th[word] # if the word is a recorded Chinese word
									continue
								except:
									word_split = word.split("-")
									if len(word_split) > 1: # pass if it is in the form of "a-b"
										continue
									elif isAlpha(word.replace("'","")): # words like o'clock
										continue
									else:
										if len(word) > 4 and isAlpha(word) == False:
											unparse = True
											break

					if unparse:
						text_unparse += [sentence_origin]
					else:
						sentence_cur = " ".join(info_cur) + " " + " ".join(words_cur)
						text += [sentence_cur]
						text_all += [sentence_cur]
						words_all += words_cur
    
				f.close()
            
			#save files without unparsed lines
			dir_save = dir + newfolder
			with codecs.open(dir_save+filename, 'w', 'utf-8') as f:
				for line in text:
					f.write(line + "\n")
			f.close()

with codecs.open(dir_lang+'unparsed.txt', 'w', 'utf-8') as f:
    for line in text_unparse:
        f.write(line + "\n")
    f.close()

with codecs.open(dir_lang+'text.txt', 'w', 'utf-8') as f:
    for line in text_all:
        f.write(line + "\n")
    f.close()
            
print("Finish reading lines")
print("Number of segmented utterance: "+str(len(text_all)))
print("Number of unsegmented utterance: "+str(len(text_unparse)))


#### output phones ####
# output silence_phones.txt
with codecs.open(dir_lang+'silence_phones.txt', 'w', 'utf-8') as f:
    f.write('SIL\n')
    for k,v in d_waste2idx.items():
        f.write(v + "\n")
f.close()
print("Finish writing silence_phones.txt")

# nonsilence phones can be generated using shell script code

#### filter and output lexicon ####
words_all = [word.upper() for word in words_all]
words_all_uniq = list(set(words_all))
words_oov = []
d_train = dict()
for word in words_all_uniq:
    try:
        d_train[word] = d_cmu[word]
        for i in range(1,max_num+1):
            try:
                d_train[word+"(i)"] = d[word+"(i)"]
            except:
                break
    except:
        try:
            d_train[word] = d_th[word]
        except:
            words_oov += [word]
            continue
print("Finish lexicon filtering")
print("Number of words used: " + str(len(words_all)))
print("Number of unique words used: " + str(len(words_all_uniq)))
print("Number of unique words in filtered lexicon file: " + str(len(d_train)))

# output lexicon.txt
lexicons = [str(k) + " " + str(v) + "\n" for k,v in d_train.items()]

with codecs.open(dir_lang+'lexicon.txt', 'w', 'utf-8') as f:
    f.write('<oov> <oov>\n')
    for lexicon in lexicons:
        f.write(lexicon)
    #for word in words_oov:
    #    f.write(str(word) + " " + "<oov>\n")
    for k,v in d_waste2idx.items():
        f.write(v + " sil" + "\n")
        
f.close()

print("Finish writing lexicon.txt")