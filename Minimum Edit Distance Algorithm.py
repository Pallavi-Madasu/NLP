class med:

    def  minEditDistR(self, target, source):
       """ Minimum edit distance. Straight from the recurrence. """

       i = len(target); j = len(source)

       if i == 0:  return j
       elif j == 0: return i

       return(min(self.minEditDistR(target[:i-1],source)+1,
                  self.minEditDistR(target, source[:j-1])+1,
                  self.minEditDistR(target[:i-1], source[:j-1])+self.substCost(source[j-1], target[i-1])))

    def substCost(self,x,y):
        if x == y: return 0
        else: return 2

med = med()
print med.minEditDistR('execution','intention')
