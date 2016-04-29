import re
import collections
from itertools import islice, izip
from collections import defaultdict
import cPickle as pickle
from numpy import matrix,linalg
import numpy
from math import log

#Inputs
fTraining = open("gene.train.txt","r")
fTest = open("HW4-test.txt","r")
fOutput = open("madasu-pallavi-assgn4-out.txt","w")

#Tag transition probabilities
word_tag_dict = dict()
prob_word_tag_dict = dict()
tag_trans_prob_dict= dict()
list_tags = ['O','I','B']
countS = 0
countB = 0
countI = 0
countO = 0

#Forming Dictionaries
listWords = []
listTags = []
for line in fTraining.readlines():
    if line == '\n':
        listWords.append('')
        listTags.append('<s>')
        countS += 1
    else:
        line = line.split()
        word = line[0]
        tag = line[1]
        print word+' - '+tag
        #word = word.lower()
        listWords.append(word)
        listTags.append(tag)
        if tag == 'I':
            countI += 1
        elif tag == 'O':
            countO += 1
        elif tag == 'B':
            countB += 1
        
        # Word Tag Dictionary
        if (word,tag) in word_tag_dict.keys():
            word_tag_dict[(word,tag)] += 1
        else:
            word_tag_dict[(word,tag)] = 1

print countI
print countO
print countB
print countS
#print word_tag_dict

#Calculate bigram counts of tags and tag transition probabilities
unigram_tag_dict = {'I': countI, 'O': countO,'B': countB, 'S': countS}
bigramTagCounts = collections.Counter(izip(listTags, islice(listTags, 1, None)))

tag_trans_prob_dict[('S','I')] = bigramTagCounts[('I','<s>')]/float(countI) # S given I, current tag given pre tag
tag_trans_prob_dict[('S','O')] = bigramTagCounts[('O','<s>')]/float(countO)
tag_trans_prob_dict[('S','B')] = bigramTagCounts[('B','<s>')]/float(countB)
tag_trans_prob_dict[('S','S')] = 0 #bigramTagCounts[('<s>','<s>')]/float(countS)

tag_trans_prob_dict[('I','O')] = 0 #bigramTagCounts[('O','I')]/float(countO)
tag_trans_prob_dict[('I','B')] = bigramTagCounts[('B','I')]/float(countB)
tag_trans_prob_dict[('I','S')] = 0 #bigramTagCounts[('<s>','I')]/float(countS)
tag_trans_prob_dict[('I','I')] = bigramTagCounts[('I','I')]/float(countI)

tag_trans_prob_dict[('B','I')] = 0 #bigramTagCounts[('I','B')]/float(countI)
tag_trans_prob_dict[('B','O')] = bigramTagCounts[('O','B')]/float(countO)
tag_trans_prob_dict[('B','S')] = bigramTagCounts[('<s>','B')]/float(countS)
tag_trans_prob_dict[('B','B')] = 0 #bigramTagCounts[('B','B')]/float(countB)

tag_trans_prob_dict[('O','I')] = bigramTagCounts[('I','O')]/float(countI)
tag_trans_prob_dict[('O','B')] = bigramTagCounts[('B','O')]/float(countB)
tag_trans_prob_dict[('O','S')] = bigramTagCounts[('<s>','O')]/float(countS)
tag_trans_prob_dict[('O','O')] = bigramTagCounts[('O','O')]/float(countO)

#tag_trans_prob_dict[('S','S')] = 0
#tag_trans_prob_dict[('I','O')] = 0
#tag_trans_prob_dict[('I','S')] = 0
#tag_trans_prob_dict[('B','I')] = 0
#tag_trans_prob_dict[('B','B')] = 0


print tag_trans_prob_dict

#Reading test file
testFile = fTest.readlines()
for line in testFile:
    if line != '\n':
        word = line.strip().split()[0]
        for tag in list_tags:
            if (word,tag) in word_tag_dict.keys():
                count_word_tag = word_tag_dict[word,tag]+1
            else:
                count_word_tag = 1 # Add-1 smoothing
                
            prob_word_tag = float(count_word_tag)/unigram_tag_dict[tag]
            prob_word_tag_dict[word,tag] = prob_word_tag

print prob_word_tag_dict

def extractSentences():
    listOfSentences = []
    listOfWordsInSentence = []
    for line in testFile:
        if line != '\n':
            word = line.strip().split()[0]
            listOfWordsInSentence.append(word)
        if(line == '\n'):
            listOfSentences.append(listOfWordsInSentence)
            listOfWordsInSentence = []
    return listOfSentences

# Viterbi
def viterbi():
    listOfSentences =  extractSentences()
    for sentence in listOfSentences: # O, I, B - Sequence
        listFinalTagSeq = []
        viterbiTable = [[0 for x in range(len(sentence))] for x in range(3)]
        backPointerTable = [[0 for x in range(len(sentence))] for x in range(3)]
        # Initialisation
        prob_start = [tag_trans_prob_dict[('O','S')],tag_trans_prob_dict[('I','S')],tag_trans_prob_dict[('B','S')]] #prob_start = [0,0.9457,0.05429]        
        for i in range(len(list_tags)):
            viterbiTable[i][0] = prob_start[i] * prob_word_tag_dict[sentence[0],list_tags[i]]

        # Main
        for wordIndex in range(1,len(sentence)):
            for tagIndex in range(len(list_tags)):
                prob_O = float(viterbiTable[0][wordIndex-1]) * float(prob_word_tag_dict[sentence[wordIndex],list_tags[tagIndex]]) * float(tag_trans_prob_dict[list_tags[tagIndex],'O'])
                prob_I = float(viterbiTable[1][wordIndex-1]) * float(prob_word_tag_dict[sentence[wordIndex],list_tags[tagIndex]]) * float(tag_trans_prob_dict[list_tags[tagIndex],'I'])
                prob_B = float(viterbiTable[2][wordIndex-1]) * float(prob_word_tag_dict[sentence[wordIndex],list_tags[tagIndex]]) * float(tag_trans_prob_dict[list_tags[tagIndex],'B'])

                p_O = float(viterbiTable[0][wordIndex-1]) * float(tag_trans_prob_dict[list_tags[tagIndex],'O'])
                p_I = float(viterbiTable[1][wordIndex-1]) * float(tag_trans_prob_dict[list_tags[tagIndex],'I'])
                p_B = float(viterbiTable[2][wordIndex-1]) * float(tag_trans_prob_dict[list_tags[tagIndex],'B'])
                
                viterbiTable[tagIndex][wordIndex] = max(prob_O,prob_I,prob_B)
                backPointerTable[tagIndex][wordIndex] = numpy.argmax([p_O,p_I,p_B])

        a = viterbiTable[0][len(sentence)-1]*float(tag_trans_prob_dict[('S','O')])
        b = viterbiTable[1][len(sentence)-1]*float(tag_trans_prob_dict[('S','I')])
        c = viterbiTable[2][len(sentence)-1]*float(tag_trans_prob_dict[('S','B')])
        
        prevTag = numpy.argmax([a,b,c])
        listFinalTagSeq.append(list_tags[prevTag])
        tagSeq = list_tags[prevTag]

        for pointer in range(len(sentence)-1,0,-1):
            prevTag = backPointerTable[prevTag][pointer]
            tagSeq = tagSeq +'-'+ list_tags[prevTag]
            listFinalTagSeq.append(list_tags[prevTag])

        # Reverse final Tag Sequence
        tagSeq = tagSeq[::-1]
        listFinalTagSeq.reverse()
        
        #Print viterbiTable
        #for row in viterbiTable:
            #print row

        #Write to output file
        for i in range(len(sentence)):
            outputStr = sentence[i] +'\t'+listFinalTagSeq[i]
            print outputStr
            fOutput.write(outputStr+'\n')
        fOutput.write('\n')

viterbi()
fTraining.close()
fTest.close()
fOutput.close()


    


