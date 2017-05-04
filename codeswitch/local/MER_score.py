#!/usr/bin/env python3
import sys
import os
from collections import defaultdict
import numpy as np

__author__="Emily Hua"
def get_file_list(path, extension):
    files = os.listdir(path)
    files = [f for f in files if f.endswith(extension)]
    print (files)
    return files

def gen_symbol_map(data_dir):
    r"""
    Returns
    -------
    dic : defaultdict
      a dictionary with key as word symbol and value as the corresponding word
      e.g. '3': 'ABACK' 
    """
    dic = defaultdict(str)
    words_path = data_dir + "/words.txt"
    # words_path = "/data/lang/words.txt"
    # words_path = "/scoring/scoring/words.txt"
    with open(parent_path + words_path, "r") as inputfile:
        for line in inputfile:
            word = line.split(" ")[0]
            symbol = line.strip("\n").split(" ")[1]
            dic[symbol] = word
    return dic
    
def gen_ground_truth_map(model):
    r"""
    Returns
    -------
    dic : defaultdict
      a dictionary with utterance id as key and groud truth transcript as its value 
    """
    dic = defaultdict(list)
    filt_path = "/exp/" + model + "/decode/scoring/test_filt.txt"
    #filt_path = "/scoring/scoring/test_filt.txt"
    with open(parent_path + filt_path, "r") as inputfile:
        for line in inputfile:
            utterance_id = line.split(" ")[0]
            words = line.strip("\n").split(" ")[1:]
            dic[utterance_id] = words
    return dic

# modified from https://segmentfault.com/q/1010000000732038, coauthor:Wendy Wang
# to detect english character and hyphen and ' and . ONLY
def isAlphahyphen(word):
    try:
        float(word)
        return True
    except:
        if word == '-':
            return True
        elif word == "'":
            return True
        elif word == "'":
            return True   
        else:
            try:
                return word.replace('-','').replace("'",'').replace('.','').encode('ascii').isalnum()
            except UnicodeEncodeError:
                if word == '-':
                    return True
                else:
                    return False
def split2(test):
    '''split chinese words into character e.g. ["我睡了","okay"] -> ["我", "睡", "了", "okay"]
    Returns
    -------
    newr : list 
      a list of english word and chinese characters 
    '''
    newr = []
    for ele in test:
        if not isAlphahyphen(ele) and len(ele) > 1:
            newr += list(ele)
        else:
            newr += [ele]
    return newr

def file_level_MER(stacked):
    r""" calculate file level stats, sum over all sentence level stats
    Returns
    -------
    ret : list
       MER, sumed Ins, sumed Sub, sumed Del, sumed eng ins, \ 
       sumed eng sub, sumed eng del, sumed che ins, sumed che sub, sumed che del on file level 
    
    """
    var_map = {'WER': 0, 'Ins' : 1, 'Sub' : 2, 'Del' : 3, 'Eng Ins' : 4, 'Eng Sub' : 5, 'Eng Del' : 6,
             'Che Ins' : 7, 'Che Sub' : 8, 'Che Del' : 9, 'Total Eng' : 10, 'Total Che' : 11}
    stacked = stacked[1:]
    sums = np.sum(stacked, axis=0)
    print("sums: ", sums)
    N = sums[var_map['Total Eng']] + sums[var_map['Total Che']]
    print ( N)
    eng_ins = sums[var_map['Eng Ins']] / N
    eng_sub = sums[var_map['Eng Sub']] / N
    eng_del = sums[var_map['Eng Del']] / N
    che_ins = sums[var_map['Che Ins']] / N
    che_sub = sums[var_map['Che Sub']] / N
    che_del = sums[var_map['Che Del']] / N    
    MER = sums[var_map['WER']] / N
    ret = [MER, sums[var_map['Ins']]/N, sums[var_map['Sub']]/N, sums[var_map['Del']]/N, 
           eng_ins, eng_sub, eng_del, che_ins, che_sub, che_del]
    return ret
           
def single_sentence_mer(ref, hyp, useChar, debug=False): #character level for Chinese
    r"""WER calculated using Levenshtein distance
    adapted from http://progfruits.blogspot.com/2014/02/word-error-rate-wer-and-word.html
    author : spacePineapple, Emily Hua
    """
    # print(useChar == False)
    if (useChar == "True"):
        r = split2(ref)
        h = split2(hyp)
    else:
        #print("no")
        r = ref
        h = hyp       

    counter = 0 # counter index out of bound, rare case 
    totalEng = len([ele for ele in r if isAlphahyphen(ele)])
    totalChe = len(r) - totalEng
    #costs will holds the costs, like in the Levenshtein distance algorithm
    costs = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]
    # backtrace will hold the operations we've done.
    # so we could later backtrace, like the WER algorithm requires us to.
    backtrace = [[0 for inner in range(len(h)+1)] for outer in range(len(r)+1)]
 
    OP_OK = 0
    OP_SUB = 1
    OP_INS = 2
    OP_DEL = 3
    SUB_PENALTY = 1
    INS_PENALTY = 1
    DEL_PENALTY = 1
    # First column represents the case where we achieve zero
    # hypothesis words by deleting all reference words.
    for i in range(1, len(r)+1):
        costs[i][0] = DEL_PENALTY*i
        backtrace[i][0] = OP_DEL
         
    # First row represents the case where we achieve the hypothesis
    # by inserting all hypothesis words into a zero-length reference.
    for j in range(1, len(h) + 1):
        costs[0][j] = INS_PENALTY * j
        backtrace[0][j] = OP_INS
     
    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                costs[i][j] = costs[i-1][j-1]
                backtrace[i][j] = OP_OK
            else:
                substitutionCost = costs[i-1][j-1] + SUB_PENALTY # penalty is always 1
                insertionCost    = costs[i][j-1] + INS_PENALTY   # penalty is always 1
                deletionCost     = costs[i-1][j] + DEL_PENALTY   # penalty is always 1
                 
                costs[i][j] = min(substitutionCost, insertionCost, deletionCost)
                if costs[i][j] == substitutionCost:
                    backtrace[i][j] = OP_SUB
                elif costs[i][j] == insertionCost:
                    backtrace[i][j] = OP_INS
                else:
                    backtrace[i][j] = OP_DEL
                 
    # back trace though the best route:
    i = len(r)
    j = len(h)
    numSub = 0
    numDel = 0
    numIns = 0
    numCor = 0
    engOkay = 0
    cheOkay = 0
    engSub = 0
    cheSub = 0
    engDel = 0
    cheDel = 0
    engIns = 0
    cheIns = 0
    if debug:
        print("OP\tREF\tHYP")
        lines = []
    while i > 0 or j > 0:
        if backtrace[i][j] == OP_OK:
            numCor += 1
            i-=1
            j-=1
            if isAlphahyphen(r[i]): # is english
                if debug:
                    lines.append("Eng OK\t" + r[i]+"\t"+h[j])
                engOkay += 1
            else:
                if debug:
                    lines.append("Che OK\t" + r[i]+"\t"+h[j])
                cheOkay += 1 
            #lines.append("OK\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_SUB:
            numSub +=1
            i-=1
            j-=1
            
            if isAlphahyphen(r[i]): # is english
                if debug:
                    lines.append("Eng SUB\t" + r[i]+"\t"+h[j])
                engSub += 1 
            else: 
                if debug:
                    lines.append("Che SUB\t" + r[i]+"\t"+h[j])
                cheSub += 1
            #lines.append("SUB\t" + r[i]+"\t"+h[j])
        elif backtrace[i][j] == OP_INS:
            numIns += 1
            j-=1
            if i < len(r):
                if isAlphahyphen(r[i]): # is english
                    if debug:
                        lines.append("Eng INS\t" + r[i]+"\t"+h[j])
                    engIns += 1
                else: 
                    if debug:
                        lines.append("Che INS\t" + r[i]+"\t"+h[j])
                    cheIns += 1
            else:
                counter += 1
                #print (counter)
                if isAlphahyphen(r[i-1]):
                     engIns += 1
                else:
                     cheIns += 1
            #lines.append("INS\t" + "****" + "\t" + h[j])
        elif backtrace[i][j] == OP_DEL:
            numDel += 1
            i-=1
            if i < len(r):
                if isAlphahyphen(r[i]): # is english
                    if debug:
                        lines.append("Eng DEL\t" + r[i]+"\t"+h[j])
                    engDel += 1
                else: 
                    if debug:
                        lines.append("Che DEL\t" + r[i]+"\t"+h[j])
                    cheDel += 1
            else:
                #print (counter)
                counter += 1
                if isAlphahyphen(r[i-1]):
                    engDel += 1
                else:
                    cheDel += 1
            #lines.append("DEL\t" + r[i]+"\t"+"****")
    if debug:
        lines = reversed(lines)
        for line in lines:
            print(line)
        print("#cor " + str(numCor))
        print("#sub " + str(numSub))
        print("#del " + str(numDel))
        print("#ins " + str(numIns))
    wer_result =  numSub + numDel + numIns
    #print ("index out of bound {} times".format(counter))
    return {'WER':wer_result, 'Cor':numCor, 'Sub':numSub, 'Ins':numIns, 
            'Del':numDel, "Eng Sub": engSub, "Eng Ins": engIns, "Eng Del": engDel, "Eng Cor": engOkay,
             'Che Sub': cheSub, "Che Ins": cheIns, "Che Del": cheDel, "Che Cor: ": cheOkay,
           "Total Eng": totalEng, "Total Che": totalChe, "out of bounds" : counter}


data_dir = sys.argv[2]
model = sys.argv[1]
useChar = sys.argv[3]
print("use Char " + useChar)
parent_path = os.path.split(os.getcwd())[0]
print ("parent path is {}".format(parent_path))
tra_path = parent_path + "/exp/" + model + "/decode/scoring/"
#tra_path = parent_path + "/exp/tri2b/decode/scoring/"
#tra_path = parent_path + "/scoring/scoring/"
tra_files = get_file_list(tra_path, ".tra") #need to get tri2b from terminal
s2w = gen_symbol_map(data_dir)
truth_map = gen_ground_truth_map(model)

variables_map  = {'WER':0, 'Ins':1, 'Sub':2, 'Del':3, 'Eng Ins':4, 'Eng Sub':5, 'Eng Del':6,
             'Che Ins':7, 'Che Sub':8, 'Che Del':9, 'Total Eng':10, 'Total Che':11}
variables = ['WER', 'Ins', 'Sub', 'Del', 'Eng Ins', 'Eng Sub', 'Eng Del',
             'Che Ins', 'Che Sub', 'Che Del', 'Total Eng', 'Total Che']
stacked = [0]*len(variables)
stats_stacked = [0]*10
counter = 0
for f in tra_files:
    with open(tra_path + f, "r") as inputfile:
        stacked = [0]*len(variables)
        for line in inputfile:
            
            #print ("\n" + line)
            symbols = line.replace("\n", "").split(" ")[1:]
            #print (symbols)
            decoded_words = [s2w[sym] for sym in symbols][:-1] # remove "" caused by newline 
            #print (decoded_words)
            true_words = truth_map[line.split(" ")[0]]
            #print (true_words)
            merret = single_sentence_mer(true_words, decoded_words, useChar, debug=False) #r,h
            #print (merret)
            processed = [merret[var] for var in variables]
            #print (processed)
            stacked = np.vstack((stacked, processed))
    stacked = stacked[1:]
    # print (stacked.shape)
    stats = file_level_MER(stacked)
    # print (stats)
    stats_stacked = np.vstack((stats_stacked, stats))  
# stats_stacked contains:    
#[chi_WER, eng_WER, sil_WER, MER]
stats_stacked = stats_stacked[1:]
means = np.mean(stats_stacked, axis=0)
maxs = np.max(stats_stacked, axis=0)
mins_index = np.argmin(stats_stacked[:,variables_map['WER']], axis=0)
min_MER = stats_stacked[mins_index][variables_map['WER']]
min_ins = stats_stacked[mins_index][variables_map['Ins']]
min_sub = stats_stacked[mins_index][variables_map['Sub']]
min_del = stats_stacked[mins_index][variables_map['Del']]
min_eng_ins = stats_stacked[mins_index][variables_map['Eng Ins']]
min_eng_sub = stats_stacked[mins_index][variables_map['Eng Sub']]
min_eng_del = stats_stacked[mins_index][variables_map['Eng Del']]
min_che_ins = stats_stacked[mins_index][variables_map['Che Ins']]
min_che_sub = stats_stacked[mins_index][variables_map['Che Sub']]
min_che_del = stats_stacked[mins_index][variables_map['Che Del']]

print ("\naverage: MER {:.3f} ".format(means[0]))
print ("\nmin: MER {:.3f},\n OVERALL INS {:.3f}, OVERALL SUB {:.3f}, OVERALL DEL {:.3f},\n \
 ENG INS {:.3f}, ENG SUB {:.3f},ENG DEL {:.3f}, \n \
 CHE INS {:.3f}, CHE SUB {:.3f}, CHE DEL {:.3f}\n ".format(min_MER, min_ins, min_sub, min_del, min_eng_ins, min_eng_sub, min_eng_del, min_che_ins, min_che_sub,  min_che_del))

print ('{0:<8}      {1:<8}     {2:<8}    {3:<8}'.format("OVERALL", "ENG", "CHE", "TYPE"))
    
for args in ( (min_ins, min_eng_ins, min_che_ins, "INS" ), 
             (min_sub, min_eng_sub, min_che_sub, "SUB"), (min_del, min_eng_del, min_che_del, "DEL")):
    print ('{0:.3f}        {1:.3f}         {2:.3f}      {3:<8}'.format(*args))
# print ("\n min: MER {:.3f}, eng_WER: {:.3f} , min_WER: {:.3f} ".format(mins[0], mins[1], mins[-1]))
# print ("\n max: chi_WER {:.3f}, eng_WER: {:.3f} , max_WER: {:.3f} ".format(maxs[0], maxs[1], maxs[-1]))



