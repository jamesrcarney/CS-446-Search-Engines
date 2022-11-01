import json
import gzip
from operator import index
import os
import sys
import matplotlib.pyplot as plt
import time

from sqlalchemy import distinct

class PostingList:
    def __init__(self, pID, sID, sNum, p, sf, pf):
        self.playId = pID
        self.sceneId = sID
        self.sceneNum = sNum
        self.pos = p
        self.sceneFreq = sf
        self.playFreq = pf

def indexer(inputFile):
    map = {}

    file = gzip.open(inputFile, "rt", encoding="utf-8")
    scenes = json.loads(file.read())
    file.close()
    sceneList = scenes["corpus"]
    sceneIndex = {}
    for index in range(0, len(sceneList)):
        list = sceneList[index]["text"].split()
        sceneIndex[sceneList[index]["sceneId"]] = index
        for i in range(0, len(list)):
            if(not list[i] in map.keys()):
                map[list[i]] = [PostingList(sceneList[index]["playId"], sceneList[index]["sceneId"], sceneList[index]["sceneNum"],  i, 0, 0)]
            else:
                map[list[i]].append(PostingList(sceneList[index]["playId"], sceneList[index]["sceneId"], sceneList[index]["sceneNum"],  i, 0, 0))
            
    return map, sceneIndex

def process_query(invertedIndex, playscene, AndOr, terms):
    ret = []
    if(playscene == "play"):
        if(AndOr == "or"):
            for term in terms:
                if(len(term.split(" ")) > 1):                    
                    init = []
                    phrase = term.split(" ")
                    playId = [p.playId for p in invertedIndex[phrase[0]]]
                    pos = [p.pos for p in invertedIndex[phrase[0]]]

                    if(len(init) == 0):
                        for i in range(0, len(playId)):
                            init.append([playId[i], pos[i]])

                    for i in range(1, len(phrase)):
                        curr = []
                        playId = [p.playId for p in invertedIndex[phrase[i]]]
                        pos = [p.pos for p in invertedIndex[phrase[i]]]

                        for index in range(0, len(playId)):
                            curr.append([playId[index], pos[index]-i])
                            
                        init = set([(i[0], i[1]) for i in init]) & set([(i[0], i[1]) for i in curr])

                    list = [i[0] for i in init]
                    
                    if(len(prev) == 0):
                        prev = list
                    else:
                        prev = [i for i in prev if i in list] 
                else:
                    list = invertedIndex[term]
                    for i in range(0, len(list)):
                        if(list[i].playId not in ret):
                            ret.append(list[i].playId)
        elif(AndOr == "and"):
            prev = []
            for term in terms:
                if(len(term.split(" ")) > 1):                    
                    init = []
                    phrase = term.split(" ")
                    playId = [p.playId for p in invertedIndex[phrase[0]]]
                    pos = [p.pos for p in invertedIndex[phrase[0]]]

                    if(len(init) == 0):
                        for i in range(0, len(playId)):
                            init.append([playId[i], pos[i]])

                    for i in range(1, len(phrase)):
                        curr = []
                        playId = [p.playId for p in invertedIndex[phrase[i]]]
                        pos = [p.pos for p in invertedIndex[phrase[i]]]

                        for index in range(0, len(playId)):
                            curr.append([playId[index], pos[index]-i])
                            
                        init = set([(i[0], i[1]) for i in init]) & set([(i[0], i[1]) for i in curr])

                    list = [i[0] for i in init]
                    
                    if(len(prev) == 0):
                        prev = list
                    else:
                        prev = [i for i in prev if i in list]                       
                else:
                    list = [i.playId for i in invertedIndex[term]]
                    if(len(prev) == 0):
                        prev = list
                    else:
                        prev = [i for i in prev if i in list]
            
            for item in prev:
                if(item not in ret):
                    ret.append(item)
    elif(playscene == "scene"):
        if(AndOr == "or"):
            for term in terms:
                if(len(term.split(" ")) > 1):                    
                    init = []
                    phrase = term.split(" ")
                    sceneId = [p.sceneId for p in invertedIndex[phrase[0]]]
                    pos = [p.pos for p in invertedIndex[phrase[0]]]

                    if(len(init) == 0):
                        for i in range(0, len(sceneId)):
                            init.append([sceneId[i], pos[i]])

                    for i in range(1, len(phrase)):
                        curr = []
                        sceneId = [p.sceneId for p in invertedIndex[phrase[i]]]
                        pos = [p.pos for p in invertedIndex[phrase[i]]]

                        for index in range(0, len(sceneId)):
                            curr.append([sceneId[index], pos[index]-i])
                            
                        init = set([(i[0], i[1]) for i in init]) & set([(i[0], i[1]) for i in curr])

                    list = [i[0] for i in init]
                    
                    if(len(prev) == 0):
                        prev = list
                    else:
                        prev = [i for i in prev if i in list] 
                else:
                    list = invertedIndex[term]
                    for i in range(0, len(list)):
                        if(list[i].sceneId not in ret):
                            ret.append(list[i].sceneId)
        elif(AndOr == "and"):
            prev = []
            for term in terms:
                if(len(term.split(" ")) > 1):                    
                    init = []
                    phrase = term.split(" ")
                    sceneId = [p.sceneId for p in invertedIndex[phrase[0]]]
                    pos = [p.pos for p in invertedIndex[phrase[0]]]

                    if(len(init) == 0):
                        for i in range(0, len(sceneId)):
                            init.append([sceneId[i], pos[i]])

                    for i in range(1, len(phrase)):
                        curr = []
                        sceneId = [p.sceneId for p in invertedIndex[phrase[i]]]
                        pos = [p.pos for p in invertedIndex[phrase[i]]]

                        for index in range(0, len(sceneId)):
                            curr.append([sceneId[index], pos[index]-i])
                            
                        init = set([(i[0], i[1]) for i in init]) & set([(i[0], i[1]) for i in curr])

                    list = [i[0] for i in init]
                    
                    if(len(prev) == 0):
                        prev = list
                    else:
                        prev = [i for i in prev if i in list] 
                else:
                    list = [i.sceneId for i in invertedIndex[term]]
                    if(len(prev) == 0):
                        prev = list
                    else:
                        prev = [i for i in prev if i in list]
            for item in prev:
                if(item not in ret):
                    ret.append(item)
    ret.sort()
    return ret

def query(invertedIndex, queriesFile, outputFolder):
    file = open(queriesFile, "r", encoding="utf-8")
    queries = file.read().split("\n")
    file.close()

    for line in queries:
        list = line.split("\t")
        queryname = list[0]
        playscene = list[1]
        AndOr  = list[2]
        ret = []

        for i in range(3, len(list)):
            ret.append(list[i])
        
        newList = process_query(invertedIndex, playscene, AndOr, ret)
        out = os.path.join(outputFolder, queryname + ".txt")
        file = open(out, "w", encoding="utf-8")
        
        for item in newList:
            file.write(item)
            file.write("\n")
        file.close()

if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'shakespeare-scenes.json.gz'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'trainQueries.tsv'
    outputFolder = sys.argv[3] if argv_len >= 4 else 'results/'
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    
    inverted, sceneIndex = indexer(inputFile)

    for term in inverted:
        list = inverted[term]
        print(term)
        for i in range(0, 1):
            print(list[i].playId)
            print(list[i].sceneId)
            print(list[i].pos)
            break
        break

    print(len(inverted["scene"]))
    # playIds = {}
    # sceneIds = {}
    # pCount = 0
    # sCount = 0

    # for term in inverted:
    #     scenes = [i.sceneId for i in inverted[term]]
    #     plays = [i.playId for i in inverted[term]]

    #     for item in plays:
    #         if item not in playIds:
    #             playIds[item] = pCount
    #             pCount += 1
        
    #     for item in scenes:
    #         if item not in sceneIds:
    #             sceneIds[item] = sCount
    #             sCount += 1

    # pCounts = [0] * len(playIds)
    # sCounts = [0] * len(sceneIds)

    # for term in inverted:
    #     list = inverted[term]
    #     count = 0
    #     for item in list:
    #         pCounts[playIds[item.playId]] += 1
        
    #     for item in list:
    #         sCounts[sceneIds[item.sceneId]] += 1

    
    # longestPlay = pCounts.index(max(pCounts))
    # longestScene = sCounts.index(max(sCounts))
    # shortestPlay = pCounts.index(min(pCounts))
    # shortestScene = sCounts.index(min(sCounts))

    # for key in playIds:
    #     if(playIds[key] == longestPlay):
    #         print("Longest Play: " + key + ": " + str(max(pCounts)))
    #     elif(playIds[key] == shortestPlay):
    #         print("Shortest Play: " + key + ": " + str(min(pCounts)))

    # for key in sceneIds:
    #     if(sceneIds[key] == longestScene):
    #         print("Longest Scene: " + key + ": " + str(max(sCounts)))
    #     elif(sceneIds[key] == shortestScene):
    #         print("Shortest Scene: " + key + ": " + str(min(sCounts)))

    # count = 0
    # sum = 0
    # for elem in sCounts:
    #     sum += elem
    #     count += 1

    # print("Average length of Scene: " + str(sum/count))

    scenes = [i.sceneId for i in inverted["you"]]
    hashYou = {}
    
    for scene in scenes:
        if(scene not in hashYou.keys()):
            hashYou[scene] = hashYou.get(scene, 0) + 1
        else:
            hashYou[scene] += 1

    scenes = [i.sceneId for i in inverted["thee"]]
    hashThee = {}
    
    for scene in scenes:
        if(scene not in hashThee.keys()):
            hashThee[scene] = hashThee.get(scene, 0) + 1
        else:
            hashThee[scene] += 1
    
    scenes = [i.sceneId for i in inverted["thou"]]
    hashThou = {}

    for scene in scenes:
        if(scene not in hashThou.keys()):
            hashThou[scene] = hashThou.get(scene, 0) + 1
        else:
            hashThou[scene] += 1
    
    combined = {} 

    for scene in scenes:
        if(scene not in combined.keys()):
            combined[scene] = hashThou.get(scene, 0) + hashThee.get(scene, 0)

    # print(len(hashYou))
    # print(len(hashThee))
    # print(len(hashThou))
    lists = sorted(hashYou.items())
    x, y = zip(*lists)
    x = [sceneIndex[i] for i in x]
    plt.bar(x, y, color="blue", label="You")
    lists = sorted(combined.items())
    x, y = zip(*lists)
    x = [sceneIndex[i] for i in x]
    plt.bar(x, y, color="red", label="Thee/Thou")
    plt.xticks([0, 100, 200, 300, 400, 500, 600, 700])
    plt.title("You vs Thee/Thou Comparison")
    plt.rc('font', size=8)
    plt.legend()
    plt.savefig("graph.png")


    

   


    #query(inverted, queriesFile, outputFolder)