class WER:
    def __init__(self):
        f1 = open("C:/Users/pallavi/Desktop/NLP/Assignment 1/assignment 1/Submission - Copy/maxmatch-answers.txt",'r')
        f2 = open("C:/Users/pallavi/Desktop/NLP/Assignment 1/assignment 1/Submission - Copy/hashtags-test-reference-2015.txt",'r')
        sum_wer = 0
        lines = f1.readlines()
        noOfLines = len(lines)
        for x in range(noOfLines):
            inputStr = lines[x].strip().lower()
            source = inputStr.split()
            referenceStr = f2.readline().strip().lower()
            target = referenceStr.split()
            print 'Source : %s' %source
            print 'Destination : %s' %target
            
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
            print 'WER is : %f' %wer 
            sum_wer = sum_wer + wer            
            avg_wer = float(sum_wer/noOfLines)
        print 'Sum of WER : %f' %sum_wer
        #print 'No of lines : %d' %noOfLines
        print 'Average Word Error Rate is : %f' %avg_wer
        f1.close()
        f2.close()

    def substCost(self,sourceStr,targetStr):
        if sourceStr == targetStr:
            return 0
        else:
            return 1
        
wer = WER()

