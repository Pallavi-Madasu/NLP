import cPickle as pickle
import nltk
from sklearn import svm,cross_validation,preprocessing,datasets,metrics
from sklearn.pipeline import make_pipeline
import string
from collections import defaultdict
from math import log
    
class SVMClassifier:
    def __init__(self):
        self.fT = open('hotelT-train.txt','r')
        self.fF = open('hotelF-train.txt','r')
        self.fTest = open('hotelDeceptionTest.txt','r')
        self.fOutput = open('madasu-pallavi-assgn3-out.txt','w')
        self.svmClassify()
        self.fT.close()
        self.fF.close()
        self.fTest.close()
        self.fOutput.close()

    # Length of the review feature
    def checkReviewlength(self,review):
        count = 0
        for word in review.strip().split():
            count += 1
        return count

    # Run the POS Tagger on the file with both True and False reviews in it and pickle the result
##    def picklePOSTags(self):
##        f = open('hotel-train.txt','r')
##        pos_dict = dict()
##        for line in f:
##            listWords = line.strip().split()
##            tokens = listWords[1:]
##            tagged_tokens = nltk.pos_tag(tokens)
##            pos_dict[listWords[0]] = tagged_tokens
##        pickle.dump(self.pos_dict, open('pos_dict.p','wb'))
##        f.close()

    #POS Tagging - Train
    def trainPosTagging(self,review):
        pos_dict = pickle.load(open('pos_dict.p', 'rb'))              
        countVerbs = 0
        countNouns = 0
        id_Review = review.strip().split()[0]
        countPos = 0
        pos = pos_dict[id_Review]
        for tuple in pos:
            countPos += 1
        for i in range(0,countPos):
            word = pos[i][0]
            posTag = pos[i][1]
            if posTag in ['VERB','VB','VBN','VBD','VBZ','VBG','VBP']:
                countVerbs += 1
            elif posTag in ['NOUN','NNP','NN','NUM','NNS','NP']:
                if word not in ['[',']']:
                    countNouns += 1
        if countVerbs > countNouns:
            feature = 0
        else:
            feature = 1
        return feature

    #POS Tagging - Test
    def testPosTagging(self,review):
            listWords = review.strip().split()
            tokens = listWords[1:]
            countVerbs = 0
            countNouns = 0
            countPos = 0
            pos = nltk.pos_tag(tokens)
            for tuple in pos:
                countPos += 1
            for i in range(0,countPos):
                word = pos[i][0]
                posTag = pos[i][1]
                if posTag in ['VERB','VB','VBN','VBD','VBZ','VBG','VBP']:
                    countVerbs += 1
                elif posTag in ['NOUN','NNP','NN','NUM','NNS','NP']:
                    if word not in ['[',']']:
                        countNouns += 1
            if countVerbs > countNouns:
                feature = 0
            else:
               feature = 1
            return feature

    # Sentiment feature
    def extractSentiment(self,review):
        sentiment_list = []
        count = 0
        listWords = review.strip().split()            
        with open("sentiment.txt") as s:
            for word in s:
                sentiment_list.append(word.strip())
        for word in listWords:
            if word in sentiment_list:
                count += 1
        return count

    def svmClassify(self):
        Xtrain=[]
        Ytrain=[]
        Xtest = []
        index = 0
        outputlist= []
        # Training True Class
        for line in self.fT:
            Ytrain.append(1)
            reviewLenFeature = self.checkReviewlength(line)
            posTagFeature = self.trainPosTagging(line)
            sentimentFeature = self.extractSentiment(line)
            Xtrain.append([reviewLenFeature,posTagFeature,sentimentFeature])
        
        # Training False Class
        for line in self.fF:
            Ytrain.append(0)
            reviewLenFeature = self.checkReviewlength(line)
            posTagFeature = self.trainPosTagging(line)
            sentimentFeature = self.extractSentiment(line)
            Xtrain.append([reviewLenFeature,posTagFeature,sentimentFeature])

        clf = make_pipeline(preprocessing.StandardScaler(), svm.SVC(C=1))
        clf.fit(Xtrain,Ytrain)

        #Classify test data
        for line in self.fTest:
            idReview = line.strip().split()[0]
            reviewLenFeature = self.checkReviewlength(line)
            posTagFeature = self.testPosTagging(line)
            sentimentFeature = self.extractSentiment(line)
            Xtest.append([reviewLenFeature,posTagFeature,sentimentFeature]) 
            result = clf.predict(Xtest[index])[0]
            if result == 0:
                outputStr = idReview + '\t' + 'F'
            else:
                outputStr = idReview + '\t' + 'T'
            self.fOutput.write(outputStr+'\n')
            outputlist.append(outputStr)
            index += 1
        ##iris = datasets.load_iris()
        ##predicted = cross_validation.cross_val_predict(clf, iris.data,iris.target, cv=10)
        ##print metrics.accuracy_score(iris.target, predicted)
        ##print cross_validation.cross_val_score(clf, iris.data, iris.target, cv=10)

    #Naive Bayes
    def naiveBayesClassify(self):
        self.fT.seek(0)
        self.fF.seek(0)
        self.fTest.seek(0)
        #Positive Class
        pos_word_Freq_Dict = dict()
        pos_word_Freq_Dict = defaultdict(lambda:0,pos_word_Freq_Dict)
        count_Pos_Words = 0
        for line in self.fT.readlines():
            listPosWords = line.strip().split()[1:]
            for word in listPosWords:
                word = self.removePunctuation(word.strip().lower())
                if not word.isdigit():
                    pos_word_Freq_Dict[word] += 1
                    count_Pos_Words += 1

        #Negative Class
        neg_word_Freq_Dict = dict()
        neg_word_Freq_Dict = defaultdict(lambda:0,neg_word_Freq_Dict)
        count_Neg_Words = 0
        for line in self.fF.readlines():
            listNegWords = line.strip().split()[1:]
            for word in listNegWords:
                word = self.removePunctuation(word.strip().lower())
                if not word.isdigit():
                    neg_word_Freq_Dict[word] += 1
                    count_Neg_Words += 1

        #Vocabulary
        total_words_list = pos_word_Freq_Dict.keys() + neg_word_Freq_Dict.keys()
        vocab_words_list = []
        stop_Words_Freq = []
        stop_words_list = []
        vocab_count = 0
        vocab_Freq_Dict = dict()
        vocab_Freq_Dict = defaultdict(lambda:0,vocab_Freq_Dict)
        for word in total_words_list:
            if word not in vocab_words_list:
                vocab_words_list.append(word)
                vocab_count += 1
        for word in vocab_words_list:
            vocab_Freq_Dict[word] = pos_word_Freq_Dict[word] + neg_word_Freq_Dict[word]
        sorted_Vocab_List = sorted(vocab_Freq_Dict.items(), key=lambda item: item[1], reverse=True)
        stop_Words_Freq = sorted_Vocab_List[:170]
        for tup in stop_Words_Freq:
            stop_words_list.append(tup[0])
            
       #Classify test data
        c1 = 0
        c2 = 0
        for testCase in self.fTest:
            lW = testCase.strip().split()
            idReview = lW[0]
            listWords = lW[1:]
            sum_Pos = 0
            sum_Neg = 0
            for word in listWords:
                word = self.removePunctuation(word.strip().lower())
                if word not in stop_words_list and not word.isdigit() and not word[0].isdigit():
                    loglikelihood_Pos = log(pos_word_Freq_Dict[word]+1) - log(count_Pos_Words+vocab_count)
                    loglikelihood_Neg = log(neg_word_Freq_Dict[word]+1) - log(count_Neg_Words+vocab_count)
                    sum_Pos += loglikelihood_Pos
                    sum_Neg += loglikelihood_Neg
                
            if sum_Pos > sum_Neg:
                result = 'T'
            else:
                result = 'F'
            outputStr = idReview + '\t' + result
            self.fOutput.write(outputStr+'\n')

    def removePunctuation(self,word):
        for ch in string.punctuation:
            word = word.replace(ch,"")
        return word

s = SVMClassifier()
