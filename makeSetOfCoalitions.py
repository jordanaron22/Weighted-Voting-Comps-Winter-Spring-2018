from copy import deepcopy
n=4#number of voters
voterList = ['A', 'B', 'C', 'D', 'E', 'F'] #ordered list of voters up to n=6


class Coalition(): #This is a class which holds 
    def __init__ (self): #there are several ways to represent a coalition
        self.data = []   #the voters in the coalition by name 'A', 'B' ect (always from largest to smallest)
        self.ranks = [] #the voters by their rank A = n, B = n-1, ...
        self.binary = None #will hold binary sequence indicating which elements are in the coalition
    
    #always enter coalitions from Largest to samllest voter weights (i.e in alphabetical order)
    def defineCoalition(self, coalition):
        self.data.extend(coalition)
        tempBinary = ['0']*n #list which will later become a binary string
        for i in range(0, len(self.data)): 
            element = self.data[i]
            k=0
            for j in range(k, n):
                if element == voterList[j]:
                    self.ranks.append(n-j) #adds the rank representation
                    tempBinary[i] = '1' #fills in the binary representation
                    k=j
        self.binary = ''.join(tempBinary) #takes list of 0s and 1s and makes a string
    
    #enter a binary string indicating which elements are in the coalition. '0101' = ['B', 'D'] Note the length of the string must = n, 
    def defineCoalitionBin(self, coalitionBin): 
        self.binary = coalitionBin
        for i in range(0, n):
            element = coalitionBin[i]
            if element == '1':
                self.data.append(voterList[i]) # makes representation with letters
                self.ranks.append(n-i)

    def __len__(self):
         return len(self.data)
    
    def __lt__(self, other): #note a coalition is less than itself
        if len(self) > len(other): #so we don't get index out of bound errors
            return False
        else:
            #does a pairwise comparison of each element in self and other
            for i in range(0,len(self)): 
                #if any element of self bigger than its pair self is not smaller than other
                if (self.ranks[i] > other.ranks[i]): 
                    return False
        return True
    
    def __eq__(self, other):
        if (self.data ==other.data): #TODO chect this is really checking elementwise it might be just checking label in memory
            return True
        return False
        
    #if self is neither less than nor grater than other they are ambiguous    
    def isAmbiguous(self, other): 
        if self < other: 
            return False
        if other < self:
            return False
        return True
    
    def isComplement(self, other): 
        for element in self.data:
            for otherElement in other.data:
                #if some element in self appears in other than they are not in each other's complements.
                if element == otherElement:
                    return False
        return True
                           
    def __str__(self):
        return str(self.data)


#we remove ambigouse coalitions that cannot be in the same coalition (are complements)
def ambiguousCoalitionDict(): 
    #empty dictionary. Keys will be a coalition with the entry being the list of all the coalitions that are ambiguous with it. All stored as binary strings
    ambiguousCoalitions = {}  
    #check all the subsets of the voters. Use binary representation to do the
    for i in range(1, 2**n):          
        self = Coalition() ##check if this will clog up memory
        self.defineCoalitionBin(format(i, '0' + str(n) + 'b')) #make coalition from binary string 
        #format command converts int to string binary with n digits
        ambigI = [] #empty list for ambiguous coalitions
        for j in range(1, 2**n): 
            other = Coalition() 
            other.defineCoalitionBin(format(j, '0' + str(n) + 'b'))
            if self.isAmbiguous(other): #check if self and other are ambiguous
                if not other.isComplement(self): #we do not want to include complements
                    ambigI.append(format(j, '0' + str(n) + 'b')) 
        if not (not ambigI): #check if ambig is empty
            ambiguousCoalitions[format(i, '0' + str(n) + 'b')] = ambigI 
    return ambiguousCoalitions

#TODO make list of ambiguous coalitions all of the same size


#TODO - could imeadiatly make this better by removing all coalitions that are smaller than their complement

def allCollections(ambiguousCoalitions):
    collectionList = [] #returns list of collections 
    for i in range(1, 2**n):
        print(str(i)+'#######################') #just to mark time
        smallestBin = format(i, '0' + str(n) + 'b')
        smallest = Coalition()
        smallest.defineCoalitionBin(smallestBin) 
        if smallestBin in ambiguousCoalitions: #Find list of all coalitions ambiguous to smallest
            ambig = ambiguousCoalitions[smallestBin]
        else:
            ambig = [smallestBin] #if no ambiguous coalitions only include smalles
        m = len(ambig)
        smallAmbig = [smallest]
        print('ambig subset selection' + str(m))
        for k in range(0, 2**m): #iterate through all subsets of the ambiguous coalitions
            selectAmbig = format(k, '0' + str(m) + 'b') #select subset of ambig
            print(selectAmbig)
            collection = []
            bigEnough = True #want to make sure that we don't include a coalition where the smallest element has a problem with complements
            for l in range(0, m): #make list of coalitions in selected subset of ambig
                if selectAmbig[l] == '1':
                    newCoalition = Coalition()
                    newCoalition.defineCoalitionBin(ambig[l])
                    smallAmbig.append(newCoalition)
            for j in range(1, 2**n): #Now check which other coalitions are forced to be included in this collection
                for small in smallAmbig:
                    other = Coalition()
                    other.defineCoalitionBin(format(j, '0' + str(n) + 'b'))
                    #other must be included if its bigger than anything in the subset of ambig
                    if small < other: 
                        #if other is bigger and is a complement, invalid collection
                        #TODO i think there's a missing case here what if other is a complement to some other element of ambig or the existing coalition?
                        if small.isComplement(other): 
                            bigEnough = False
                            break
                        if not (other in collection): #check if other already in the coalition
                            collection.append(other)
            if (not (collection in collectionList)) & (bigEnough):
                    collectionList.append(collection)

    return collectionList
    
def getPowerDistr(collectionList):
    powerListFrac = []
    powerListWhole = []
    #Iterate through the list of collections and find the power distr for each one.
    #TODO make seperate fun which finds power distr of a single collection
    for i in range(0, len(collectionList)): 
        collection = collectionList[i]
        powerTemp = [0]*n
        for j in range(0, len(collectionList[i])):
            coalition = collection[j]
            for k in range(0, n):
                if coalition.binary[k] == '0': 
                    powerTemp[k] = powerTemp[k] - 1
                else:
                    powerTemp[k] = powerTemp[k] + 1
        power = [x / sum(powerTemp) for x in powerTemp]
    #TODO chech if list already contains distr
        powerListFrac.append(power)
        powerListWhole.append(powerTemp)
    return powerListFrac, powerListWhole 
    
def main():
#    self = Coalition()
#    other = Coalition()
#    self.defineCoalition(['C', 'D'])
#    other.defineCoalitionBin('0011')
#    print(other)
#    print (other == self)
#    print (self < other)
#    print (self.isComplement(other))
##    print(self.isAmbiguous(other))
#    print (ambiguousCoalitionDict())  
    print(ambiguousCoalitionDict())
    test = allCollections(ambiguousCoalitionDict())
#    print(len(test))
#    for i in range(0, len(test)):
#        print('.')
#        for j in range(0, len(test[i])):
#            print(test[i][j])

#    print(getPowerDistr(test))
          
main()


