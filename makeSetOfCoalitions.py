from copy import deepcopy
n=4 #number of voters
voterList = ['A', 'B', 'C', 'D', 'E', 'F'] #ordered list of voters up to n=6


class Coalition():
    def __init__ (self):
        self.data = []   #number of voters in the system
        self.ranks = []
        self.binary = None #will hold binary sequence indicating which elements are in the coalition
        
    def defineCoalition(self, coalition): #always enter coalitions from Largest to samllest voter weights (i.e in alphabetical order)
        self.data.extend(coalition)
        tempBinary = ['0']*n 
        for i in range(0, len(self.data)):
            element = self.data[i]
            k=0
            for j in range(k, n):
                if element == voterList[j]:
                    self.ranks.append(n-j)
                    tempBinary[i] = '1'
                    k=j
        self.binary = ''.join(tempBinary)
                    
    def defineCoalitionBin(self, coalitionBin): #always enter coalitions from Largest to samllest voter weights (i.e in alphabetical order)
        self.binary = coalitionBin
        for i in range(0, n):
            element = coalitionBin[i]
            if element == '1':
                self.data.append(voterList[i])
                self.ranks.append(n-i)

    def __len__(self):
         return len(self.data)
    
    def __lt__(self, other): #note a coalition is less than itself
        if len(self) > len(other):
            return False
        else:
            for i in range(0,len(self)):
                if (self.ranks[i] > other.ranks[i]):
                    return False
        return True
    
    def __eq__(self, other):
        if (self.data ==other.data):
            return True
        return False
        
    def isAmbiguous(self, other):
        if self < other:
            return False
        if other < self:
            return False
        return True
    
    def isComplement(self, other):
        for element in self.data:
            for otherElement in other.data:
                if element == otherElement:
                    return False
        return True
                           
    def __str__(self):
        return str(self.data)


    
     
def ambiguousCoalitionDict(): ##this can be better if we remove ambigouse coalitions that cannot be in the same coalition (are complements)
    ambiguousCoalitions = {}
    for i in range(1, 2**n):          
        self = Coalition() ##check if this will clog up memory
        self.defineCoalitionBin(format(i, '0' + str(n) + 'b')) 
        #converts to string binary with n digits
        ambigI = []
        for j in range(1, 2**n): 
            other = Coalition() ##check if this will clog up memory
            other.defineCoalitionBin(format(j, '0' + str(n) + 'b'))
            if self.isAmbiguous(other):
                if not other.isComplement(self):
                    ambigI.append(format(j, '0' + str(n) + 'b')) 
        if not not ambigI:
            ambiguousCoalitions[format(i, '0' + str(n) + 'b')] = ambigI
    return ambiguousCoalitions
        
def allCoalitions(ambiguousCoalitions):
    coalitionList = []
#    z=0
#    y=0
    for i in range(1, 2**n):
        bigEnough = True
        smallestBin = format(i, '0' + str(n) + 'b')
        smallest = Coalition()
        smallest.defineCoalitionBin(smallestBin)
#        coalition = []
#        print('smallest ' + str(smallest))
#        for j in range(1, 2**n):
#            other = Coalition()
#            other.defineCoalitionBin(format(j, '0' + str(n) + 'b'))
#            print('other' + str(other))
#            if smallest < other:
#                print ('here')
#                if smallest.isComplement(other):
#                    bigEnough = False
#                    break
#                coalition.append(other)
#        if (not coalition in coalitionList) & (bigEnough):
#        #if bigEnough:
#            coalitionList.append(coalition)
#            z = z +1
        if smallestBin in ambiguousCoalitions:
            ambig = ambiguousCoalitions[smallestBin]
        else:
            ambig = [smallestBin]
        m = len(ambig)
        smallAmbig = [smallest]
        for k in range(0, 2**m):
            selectAmbig = format(k, '0' + str(m) + 'b')
            coalition = []
            bigEnough = True
            for l in range(0, m):
                if selectAmbig[l] == '1':
                    newCoalition = Coalition()
                    newCoalition.defineCoalitionBin(ambig[l])
                    smallAmbig.append(newCoalition)
            for j in range(1, 2**n):
                for small in smallAmbig:
                    other = Coalition()
                    other.defineCoalitionBin(format(j, '0' + str(n) + 'b'))
                    if small < other:
                        if small.isComplement(other):
                            bigEnough = False
                            break
                        if not (other in coalition):
                            coalition.append(other)
            if (not (coalition in coalitionList)) & (bigEnough): #if bigEnough:
                    coalitionList.append(coalition)
#                selectCoalition = deepcopy(coalition) ##keeps the damn mutable object in place 
#                goodSelect = True
#                for l in range(0,m):
#                    if select[l] == '1':
#                        newCoalition = Coalition()
#                        newCoalition.defineCoalitionBin(ambig[l])
#                        for other in selectCoalition:
#                            if (newCoalition.isComplement(other)) | (newCoalition ==other):
#                                goodSelect=False
#                                break
#                        if goodSelect:
#                            selectCoalition.append(newCoalition)

#                        if (not selectCoalition in coalitionList) & (goodSelect):
#                        #if (goodSelect):
#                            y=y+1  
#                            coalitionList.append(selectCoalition)
#        print (str(z) + '+' + str(y))
    return coalitionList
        
def main():
#    self = Coalition()
#    other = Coalition()
#    self.defineCoalition(['C', 'D'])
#    other.defineCoalitionBin('0011')
#    print(other)
#    print (other == self)
#    print (self < other)
#    print (self.isComplement(other))
#    print(self.isAmbiguous(other))
    print (ambiguousCoalitionDict())  
    test = allCoalitions(ambiguousCoalitionDict())
    print(len(test))
    for i in range(0, len(test)):
        print('.')
        for j in range(0, len(test[i])):
            print(test[i][j])

main()


