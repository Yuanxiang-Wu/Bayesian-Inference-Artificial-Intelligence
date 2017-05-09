import sys
#import time
filename=str(sys.argv[1])
with open(filename) as f:
#start = time.clock()
with open("input_1.txt") as f:
    line = f.readlines()

f = open('output.txt','w')
class Node:
    def __init__(self, line):
        if line[0].find("|") == -1:
            self.name = line[0].strip()
            self.parent = None
            self.val = float(line[1])
        else:
            str = line[0].strip().split(" | ")
            self.name = str[0]
            self.parent = str[1].split(" ")
            par_num = len(self.parent)
            self.val = []
            self.par_val = []
            for i in range(0, 2 ** par_num):
                str = line[i + 1].strip().split(" ")
                self.val.append(float(str[0]))
                self.par_val.append(str[1:])

class Query:
    def __init__(self, line):
        self.val = None
        str = line[2:len(line.strip()) - 1]
        if str.find("|") == -1:
            str1 = str.split(", ")
            varnum = len(str1)
            self.var = []
            self.var_val = []
            for i in range(0, varnum):
                str2 = str1[i].split(" = ")
                self.var.append(str2[0])
                self.var_val.append(str2[1])
            self.evidence = None
        else:
            str = str.split(" | ")
            varstr1 = str[0].split(", ")
            evistr1 = str[1].split(", ")
            varnum = len(varstr1)
            evinum = len(evistr1)
            self.var = []
            self.var_val = []
            self.evidence = []
            self.evi_val = []
            for i in range(0, varnum):
                varstr2 = varstr1[i].split(" = ")
                self.var.append(varstr2[0])
                self.var_val.append(varstr2[1])
            for i in range(0, evinum):
                evistr2 = evistr1[i].split(" = ")
                self.evidence.append(evistr2[0])
                self.evi_val.append(evistr2[1])

def getindex(Node, par, par_val):
    parlen = len(par)
    ind = []
    for i in range(0, parlen):
        for j in range(0, parlen):
            if Node.parent[j] == par[i]:
                ind.append(j)
    temp = [None for i in range(0, parlen)]
    for i in range(0, parlen):
        temp[ind[i]] = par_val[i]
    return Node.par_val.index(temp)

#when atomic event
def CalcProb(Node, var_val, par, par_val):
    if Node.parent == None:
        for i in NodeList:
            if i == Node:
                if var_val == "+":
                    return i.val
                else:
                    return 1 - i.val
    else:
        for i in NodeList:
            if i == Node:
                index = getindex(i, par, par_val)
                if var_val == "+":
                    return i.val[index]
                else:
                    return 1 - i.val[index]

num = int(line[0])
queries = []
QueryList = []
for i in range(0, num):
    queries.append(line[i + 1])
    QueryList.append(Query(queries[i].strip()))


NodeList=[]
prev = num + 1
for index in range(num + 1, len(line)):
    if line[index] == '***\n':
        s = line[prev: index]
        NodeList.append(Node(s))
        prev = index + 1

s = line[prev : len(line)]
NodeList.append(Node(s))

#main
def TrueValadd(List):
    length = len(List)
    i = length - 1
    List[i] = List[i] + 1
    while List[i] != 1:
        List[i] = 0
        List[i - 1] = List[i - 1] + 1
        i = i - 1
    return List

def isDefinit(Node, hidden):
    if hidden.count(Node) != 0:
        return False
    else:
        if Node.parent == None:
            return True
        else:
            for i in Node.parent:
                for j in hidden:
                    if i == j.name:
                        return False
            return True

product = 1
par = []
par_val = []

for step in range(0, num):
    Q=QueryList[step]
    sum = 0
    hidden = []
    varval = 0
    #alpha
    if Q.evidence == None:
        alpha = 1
    else:
        alpha_var = Q.evidence[:]
        alpha_val = Q.evi_val[:]
        indefvar = alpha_var[:]
        for i in NodeList:
            if alpha_var.count(i.name) == 0:
                hidden.append(i)
                indefvar.append(i.name)
        List1 = [0 for i in range(0, len(hidden))]
        for i in range(0, 2 ** len(hidden)):
            for j in NodeList:
                indefval = alpha_val[:]
                indefval.extend(List1)
                varval = indefval[indefvar.index(j.name)]
                if varval == 0:
                    varval = "-"
                if varval == 1:
                    varval = "+"
                if j.parent == None:
                    product = product * CalcProb(j, varval, None, None)
                else:
                    for p in j.parent:
                        for q in indefvar:
                            if p == q:
                                par.append(q)
                                if indefval[indefvar.index(q)] == 0:
                                    par_val.append("-")
                                elif indefval[indefvar.index(q)] == 1:
                                    par_val.append("+")
                                else:
                                    par_val.append(indefval[indefvar.index(q)])
                    product = product * CalcProb(j, varval, par, par_val)
                    par = []
                    par_val = []
                    indefval = []
            sum = sum + product
            product = 1
            if hidden != []:
                List1 = TrueValadd(List1)
        alpha = sum
    #print alpha

    sum = 0
    hidden = []
    varval = 0
    var = Q.var[:]
    var_val = Q.var_val[:]
    if Q.evidence != None:
        var.extend(Q.evidence)
        var_val.extend(Q.evi_val)
    factor = []
    indefvar = var[:]
    for i in NodeList:
        if var.count(i.name) == 0:
            hidden.append(i)
            indefvar.append(i.name)
    List = [0 for i in range(0, len(hidden))]
    for i in range (0, 2 ** len(hidden)):
        for j in NodeList:
            indefval = var_val[:]
            indefval.extend(List)
            varval = indefval[indefvar.index(j.name)]
            if varval == 0:
                varval = "-"
            if varval == 1:
                varval = "+"
            if j.parent == None:
                product = product * CalcProb(j, varval, None, None)
            else:
                for p in j.parent:
                    for q in indefvar:
                        if p == q:
                            par.append(q)
                            if indefval[indefvar.index(q)] == 0:
                                par_val.append("-")
                            elif indefval[indefvar.index(q)] == 1:
                                par_val.append("+")
                            else:
                                par_val.append(indefval[indefvar.index(q)])
                product = product * CalcProb(j, varval, par, par_val)
                par = []
                par_val = []
                indefval = []
        sum = sum + product
        product = 1
        if hidden != []:
            List = TrueValadd(List)
    f.write( "%.2f" % float(sum/alpha) )
    if step != num - 1:
        f.write("\n")
#print (time.clock() - start)
