import sys
import gzip
from numpy import array
from numpy.linalg import norm

def PageRank(inputFile, lambda_val, tau, inLinksFile, pagerankFile, k):
    file = gzip.open(inputFile, 'rt', encoding="utf-8")
    links = file.read()
    file.close()

    links = links.strip().split("\n")

    I = [] #initializing I (OldPR)
    R = [] #initializing R (NewPR)
    indexes = {} #stores {Page: Corresponding Index}
    P = {} #stores {Page: Target Pages}
    count = 0
    #Building P
    for line in links:
        line = line.split("\t") #Splits LINK\tPAGE
        if(len(line) == 2):#checks that the length is two
            if(line[0] != " " and line[1] != " "):#Checks both not blank
                if(line[0] not in P):#updates for unique new Pages
                    P.update({line[0]: [line[1]]})
                else:
                    P[line[0]].append(line[1])
                if(line[1] not in P):#if a page isn't a source we still flag it as one
                    P.update({line[1]: []})

    for key in P:
        indexes.update({key: count})
        count = count + 1
       
    I = [1/len(P)] * len(P) #initializing I as [1/n, 1/n, ..., 1/n]

    while True:
        sum = 0
        R = [lambda_val/len(P)]*len(P) #initializing R as [lambda/n, lambda/n, ..., lambda/n]

        for key in P:
            if(len(P[key]) != 0):#we check if there are target pages
                for outlink in P[key]:#for each page in P[key]
                    R[indexes[outlink]] = R[indexes[outlink]]+(1-lambda_val)*(I[indexes[key]]/len(P[key]))#only apply to those specific
            else:#We take a sum of the values for ALL terms
                sum += (1-lambda_val)*(I[indexes[key]])/len(P)
        for i in range(len(R)):
            R[i] += sum#Increment here for Efficiency

        if(norm(array(R) - array(I), 2) < tau):#If we are at convergence stop.
            break
        
        I = R #reset
    
    out = [] #building for page ranks
    for i in (indexes):
        out.append([i, R[indexes[i]]]) #take index and rank

    out = sorted(out, key=lambda l:l[1], reverse=True) #sort highest to lowest
    file = open(pagerankFile, "w", encoding="utf-8")
    #Write top 100 to a file
    for i in range(0, k):
        if(i < len(out)):
            file.write(str(out[i][0]))
            file.write("\t")
            file.write(str(i+1)) 
            file.write("\t")
            file.write(str(out[i][1]))
            file.write("\n")
        else:
            break
    file.close()
    
    trackCount = [0] * len(P)

    for key in P:
        for elem in P[key]:
            trackCount[indexes[elem]] += 1

    inLinks = [] #building for inlink counts
    
    for key in P:  
        inLinks.append([key, trackCount[indexes[key]]]) #take key and length of key count
    
    inLinks = sorted(inLinks, key=lambda l:l[1], reverse=True) #sort highest to lowest
    file = open(inLinksFile, "w", encoding="utf-8")
    #Write top 100 to a file
    for i in range(0, k):
        if(i < len(out)):
            file.write(str(inLinks[i][0]))
            file.write("\t")
            file.write(str(i+1)) 
            file.write("\t")
            file.write(str(inLinks[i][1]))
            file.write("\n")
        else:
            break
    file.close()

if __name__ == '__main__':
        argv_len = len(sys.argv)
        inputFile = sys.argv[1] if argv_len >= 2 else "links.srt.gz"
        lambda_val = float(sys.argv[2]) if argv_len >=3 else 0.2
        tau = float(sys.argv[3]) if argv_len >=4 else 0.005
        inLinksFile = sys.argv[4] if argv_len >= 5 else "inlinks.txt"
        pagerankFile = sys.argv[5] if argv_len >= 6 else "pagerank.txt"
        k = int(sys.argv[6]) if argv_len >= 7 else 100

        ret = PageRank(inputFile, lambda_val, tau, inLinksFile, pagerankFile, k)