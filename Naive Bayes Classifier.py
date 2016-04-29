import string
from collections import defaultdict
from math import log

class NaiveBayes:
    def __init__(self):
        fPos = open('C:/Users/pallavi/Desktop/NLP/Assignment 2/hotelPosT-train.txt','r')
        fNeg = open('C:\Users\pallavi\Desktop\NLP\Assignment 2\hotelNegT-train.txt','r')
        fTest = open('C:/Users/pallavi/Desktop/NLP/Assignment 2/HW2-testset.txt','r')
        fOutput = open('C:/Users/pallavi/Desktop/NLP/Assignment 2/madasu-pallavi-assgn2-out.txt','w')
        self.pos = 'POS'
        self.neg = 'NEG'
        
        #Positive Class
        pos_Words_List = self.getDetailsOfClass(fPos)
        self.word_Freq_Pos_Dict = self.filterVocabulary(pos_Words_List,self.pos)
        
        #Negative Class
        neg_Words_List = self.getDetailsOfClass(fNeg)
        self.word_Freq_Neg_Dict = self.filterVocabulary(neg_Words_List,self.neg)

        #Read the test cases from the file and categorize them as POS or NEG, writing the output to file
        countNeg = 0
        for testCase in fTest:
            listWords = testCase.strip().split()
            sum_pos = self.calcProbOfSentence(self.pos,listWords)
            sum_neg = self.calcProbOfSentence(self.neg,listWords)
            if sum_pos > sum_neg:
                result = self.pos
            else:
                result = self.neg
            outputStr = listWords[0] + '\t' + result
            fOutput.write(outputStr+'\n')
            print outputStr
        fPos.close()
        fNeg.close()
        fTest.close()
        fOutput.close()

    #Calculate the conditional probabilities using Bayes rule for the test cases
    def calcProbOfSentence(self,reviewType,listWords):
        sum_Counts = 0
        negativeWords = ['not','didnt','no']
        if reviewType == self.pos:
            words_Freq_Dict = self.word_Freq_Pos_Dict
        else:
            words_Freq_Dict = self.word_Freq_Neg_Dict

        for i in range(1,len(listWords)):
            #Get countof each word from the word_Freq_List                        
            word = self.removePunctuation(listWords[i].strip().lower())
            count = words_Freq_Dict[word]
            # Suppressing the effect of negative words
            if reviewType == self.pos:
                prevWord1 = self.removePunctuation(listWords[i-1].strip().lower())
                prevWord2 = self.removePunctuation(listWords[i-2].strip().lower())
                if prevWord1 in negativeWords or prevWord2 in negativeWords:
                    count = 0
            
            #find loglikelihood after add-1 smoothing, Ignoring the denominator 'no of words+vocabulary' as it will be constant for the balanced classes
            loglikelihood = log(float(count + 1))
            #Taking the sum of word counts instead of probability
            sum_Counts += loglikelihood
        return sum_Counts

    
    def getDetailsOfClass(self,f):
        list_Of_Words = []
        for doc in f.readlines():
            temp_list_Of_Words = []
            for word in doc.strip().split():
                word = self.removePunctuation(word.strip().lower())
                temp_list_Of_Words.append(word)
            temp_list_Of_Words.pop(0)
            list_Of_Words = list_Of_Words + temp_list_Of_Words
        return list_Of_Words

    def filterVocabulary(self,listWords, reviewType):
        word_Freq_Dict = {}
        word_Freq_Dict = defaultdict(lambda:0,word_Freq_Dict)

        #Adding stoplist and top frequency words which do not have any sentiment - to be ignored
        topFreqList = ['hotel','hotels','stay','ceiling','windows','floor','night','staying','staff','stayed']
        # File contains the stop list of words
        fs = open('C:/Users/pallavi/Desktop/NLP/Assignment 2/stoplist2.txt','r')
        stopList = fs.read().strip().split()
        stopList = stopList + topFreqList
        for word in listWords:
            word = self.removePunctuation(word.strip().lower())
            # Ignoring numbers
            if not word.isdigit():
                word_Freq_Dict[word] = word_Freq_Dict[word] + 1

        #Reset the count and frequency of stop words accordingly
        for w in stopList:
            w = self.removePunctuation(w.strip().lower())
            word_Freq_Dict[w] = 0
    
        #Add vocabulary
        if reviewType == self.neg:
            f1 = open('C:/Users/pallavi/Desktop/NLP/Assignment 2/neg_vocab.txt','r')
            featuredNegWords = f1.read().strip().split()
            for negWord in featuredNegWords:
                negWord = self.removePunctuation(negWord.strip().lower())
                word_Freq_Dict[negWord] = word_Freq_Dict[negWord] + 10
        else:
            f2 = open('C:/Users/pallavi/Desktop/NLP/Assignment 2/pos_vocab.txt','r')
            featuredPosWords = f2.read().strip().split()
            for posWord in featuredPosWords:
                posWord = self.removePunctuation(posWord.strip().lower())
                word_Freq_Dict[posWord] = word_Freq_Dict[posWord] + 10
            
        return word_Freq_Dict

    def removePunctuation(self,word):
        for ch in string.punctuation:
            word = word.replace(ch,"")
        return word
        
nb = NaiveBayes()
