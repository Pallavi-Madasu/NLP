import collections
import enchant

class MaxMatch:
    
    def __init__(self):
        self.dictWords = collections.OrderedDict()
        self.outputStr = ''
        dictLocation = raw_input('Please enter the location of the dictionary : ')
        hashTagFileLocation = raw_input('Please enter the location of the hashtags file to be segmented : ')
        maxMatchOutputFileLocation = raw_input('Where do you want to save the maxmatch answers: ')
        goldAnsFileLocation = raw_input('Enter the location of the file of gold answers : ')
        
        with open(dictLocation,"r") as f:
            for i in range(75000):
                line = next(f)
                self.dictWords[line.split()[0]] = line.split()[1]

        self.readFileForMaxMatch(hashTagFileLocation,maxMatchOutputFileLocation)
        print 'Average Word Error Rate is : %f' %self.calcAverageWER(maxMatchOutputFileLocation,goldAnsFileLocation)
       
    def readFileForMaxMatch(self,hashTagFileLocation,maxMatchOutputFileLocation):       # Reads file and executes maxMatch
        countSuccess = 0
        countFailure = 0
        f1 = open(hashTagFileLocation,"r")
        f2 = open(maxMatchOutputFileLocation,"w")
        lines = f1.readlines()
        noOfLinesInFile = len(lines)
        for i in range(noOfLinesInFile):
            inputStr = lines[i].strip()
            inputStr = inputStr[1:].lower()
            outputStr = self.maxMatchNew(inputStr)
            f2.write(outputStr+'\n')
        f1.close()
        f2.close()

    def maxMatchWord(self,inputStr):    # Traditional MaxMatch Implementation
        initialPtr = 1
        finalPtr = len(inputStr)
        outputStr = ''
        while initialPtr != len(inputStr):
            if(initialPtr != finalPtr):
                currentWord = inputStr[initialPtr:finalPtr]
                if currentWord in self.dictWords:
                    outputStr = outputStr +' '+ currentWord
                    initialPtr = finalPtr
                    finalPtr = len(inputStr)
                else:
                    finalPtr = finalPtr - 1
                    if initialPtr == finalPtr:
                        outputStr = outputStr +' '+ currentWord
                        initialPtr = initialPtr + 1
                        finalPtr = len(inputStr)
        return outputStr.strip()

    def maxMatchNew(self,inputStr):     # Improved Version
        output = ''
        if inputStr in self.dictWords:
            output = inputStr
            return output
        else:  
            initialPtr = 2
            found = False
            for i in range(1,len(inputStr)):
                firstWord = inputStr[:initialPtr]
                secondWord = inputStr[initialPtr:]
                if firstWord in self.dictWords and secondWord in self.dictWords:
                    found = True
                    output = firstWord + ' ' + secondWord
                    break
                else:
                    initialPtr = initialPtr + 1

            if found == False:
                initialPtr = 2
                for i in range(1,len(inputStr)):
                    firstWord = inputStr[:initialPtr]
                    if firstWord in self.dictWords:
                        secondWord = inputStr[initialPtr:]
                        subsWord = self.getSubsequentWords(secondWord)
                        if subsWord!= '':
                            output = firstWord + ' ' + subsWord
                            break
                        else:
                            initialPtr = initialPtr + 1
                    else:
                        initialPtr = initialPtr + 1

            outputMaxMatch = self.maxMatchWord('#'+inputStr)
            if output == '' or len(output.split()) > len(outputMaxMatch.split()):
                output = outputMaxMatch
            return output

    def getSubsequentWords(self,inputStr):          # Helper Function
        initialPtr = 0
        output=''
        for i in range(1,len(inputStr)):
            firstWord = inputStr[:initialPtr]
            secondWord = inputStr[initialPtr:]
            if firstWord in self.dictWords and secondWord in self.dictWords:
                output = firstWord + ' ' + secondWord
                break
            else:
                initialPtr = initialPtr + 1
        return output
            
    def calcAverageWER(self,hypoAnsFileLocation,goldAnsFileLocation):       # Calculation of WER
        f1 = open(hypoAnsFileLocation,"r")
        f2 = open(goldAnsFileLocation,"r")
        sum_wer = 0
        c1 = 0
        c2 = 0
        lines = f1.readlines()
        noOfLines = len(lines)
        for x in range(noOfLines):
            inputStr = lines[x].strip().lower()
            source = inputStr.split()
            referenceStr = f2.readline().strip().lower()
            target = referenceStr.split()
            
            n = len(target)
            m = len(source)

            distance = [[0 for i in range(m+1)] for j in range(n+1)]

            for i in range(1,n+1):
                distance[i][0] = distance[i-1][0] + 1

            for j in range(1,m+1):
                distance[0][j] = distance[0][j-1] + 1

            for i in range(1,n+1):
                for j in range(1,m+1):
                    distance[i][j] = min(distance[i-1][j]+1,distance[i][j-1]+1,distance[i-1][j-1]+self.substCost(source[j-1],target[i-1]))

            med = distance[n][m]
            noOfWords = len(referenceStr.split())
            wer = med/float(noOfWords)
            sum_wer = sum_wer + wer            
            avg_wer = float(sum_wer/noOfLines)
        f1.close()
        f2.close()
        return avg_wer

    def substCost(self,sourceStr,targetStr):        # Helper Function
        if sourceStr == targetStr:
            return 0
        else:
            return 1

mw = MaxMatch()
