from contextlib import nullcontext
from operator import truediv
import string
import re
from winreg import EnumValue
import matplotlib.pyplot as plt

def tokenization(file):
    init = open(file, "r", encoding="utf-8")
    words = init.read().lower().strip().split()
    init.close()
    ret = []
    prefix = ""

    for index in range(0, len(words)):
        temp = ""
        if(re.search("(?:[a-zA-Z]\.){2,}", words[index])):
            temp = words[index].replace(".", "").replace("'", "").replace(",", "")
            for char in temp:
                if(not char.isalpha()):
                    temp = temp.replace(char, "")
        else:
            check = words[index].replace("'", "")
            for char in check:
                if(char.isalnum()):
                    temp = temp + char
                else:
                    if(not isPrefix(temp)):
                        if(len(temp)):
                            if(len(prefix) and len(temp)):
                                ret.append(prefix + "." + temp)
                                temp = ""
                                prefix = ""
                                continue
                            else:
                                ret.append(temp)
                                temp = ""
                                continue
        if(isPrefix(temp)):
            prefix = temp
            temp = ""
            continue
        if(len(prefix) and len(temp)):
            ret.append(prefix + "." + temp)
        elif(len(temp)):
            ret.append(temp)
        prefix = ""
    return ret

def stopword(list, file):
    init = open(file, "r", encoding="utf-8")
    stopwords = init.read().lower().strip().split()
    init.close()
    ret = []

    for word in list:
        if(word not in stopwords):
            ret.append(word)
    return ret

def stemming(list):
    ret = []
    
    for index in range(len(list)):
        stem = "" 
        if(re.search("\w+sses$" , list[index])):
            stem = list[index].replace("sses", "ss")
            ret.append(stem)
            continue
        elif(re.search("\w+ies$", list[index])):
            if(len(list[index]) - 3 > 1):
                stem = list[index].replace("ies", "i")
                ret.append(stem)
                continue
            else:
                stem = list[index].replace("ies", "ie")
                ret.append(stem)
                continue
        elif(re.search("\w+ied$", list[index])):
            if(len(list[index]) - 3 > 1):
                stem = list[index].replace("ied", "i")
                ret.append(stem)
                continue
            else:
                stem = list[index].replace("ied", "ie")
                ret.append(stem)
                continue
        elif(re.search("\w+ss", list[index])):
            stem = list[index]
            ret.append(stem)
            continue
        elif(re.search("\w+us", list[index])):
            stem = list[index]
            ret.append(stem)
            continue
        elif(re.search("\w*[aeiou]+\w*.s$", list[index])):
            stem = list[index][:-1]
            ret.append(stem)
            continue
        elif(re.search("\w+eed$", list[index])):
            match = re.search("[aeiou]+[bcdfghjklmnpqrstvwxyz]+eed$", list[index])
            if(match):
                stem = list[index].replace("eed", "ee")
                ret.append(stem)
                continue
            else:
                stem = list[index]
                ret.append(stem)
                continue
        elif(re.search("\w+eedly$", list[index])):
            if(match):
                stem = list[index].replace("eedly", "ee")
                ret.append(stem)
                continue
            else:
                stem = list[index]
                ret.append(stem)
                continue
        elif(re.search("[aioubcdfghjklmnqrstvwxyz]+ed$", list[index])):
            stem = list[index].replace("ed", "")
            match = re.search("at|bl|iz$", stem)
            if(match):
                stem = stem + "e"
                ret.append(stem)
                continue
            match = re.search("ll|ss|zz$", stem)
            if(not match):
                if(getM(stem) == 1):
                    stem = stem + "e"
                ret.append(stem)
                continue
        elif(re.search("[aioubcdfghjklmnqrstvwxyz]+edly$", list[index])):
            stem = list[index].replace("edly", "")
            match = re.search("at|bl|iz$", stem)
            if(match):
                stem = stem + "e"
                ret.append(stem)
                continue
            match = re.search("ll|ss|zz$", stem)
            if(not match):
                if(getM(stem) == 1):
                    stem = stem + "e"
                ret.append(stem)
                continue
        elif(re.search("\w+ing$", list[index])):
            stem = list[index].replace("ing", "")
            match = re.search("at|bl|iz$", stem)
            if(match):
                stem = stem + "e"
                ret.append(stem)
                continue
            match = re.search("ll|ss|zz$", stem)
            if(not match):
                if(getM(stem) == 1):
                    stem = stem + "e"
                ret.append(stem)
                continue
        elif(re.search("\w+ingly$", list[index])):
            stem = list[index].replace("ingly", "")
            if(re.search("at|bl|iz$", stem)):
                stem = stem + "e"
                ret.append(stem)
                continue
            match = re.search("ll|ss|zz$", stem)
            if(match):
                stem = stem[:-1]
                ret.append(stem)
                continue
            else:
                if(getM(stem) == 1):
                    stem = stem + "e"
                ret.append(stem)
                continue
        else:
            stem = list[index]
            ret.append(stem)
            continue
    return ret

def writeTokenizedA(list):
    file = open("tokenized-A.txt", "w", encoding="utf-8")
    for word in list:
        file.write(word + "\n")
    file.close()

#PART B
def frequency(list):
    wordCount = []
    visited = []
    ret = []
    for word in list:
        if(not word in visited):
            wordCount.append((word, list.count(word)))
            visited.append(word)

    ret = sorted(wordCount, key=lambda x: (-x[1], x[0]))

    file = open("terms-B.txt", "w", encoding="utf-8")
    
    for i in range(0,300):
        file.write(str(ret[i]) + "\n")
    file.close()

def gov2(list):
    visited = []
    x = []
    y = []
    x_counter = 0
    y_counter = 0

    for word in list:
        if(not word in visited):
            y_counter = y_counter + 1
            visited.append(word)
        x_counter = x_counter + 1
        x.append(x_counter)
        y.append(y_counter)
    plt.plot(x,y)
    plt.xlabel("Words in Collection")
    plt.ylabel("Words in Vocabulary")
    plt.title("GOV2-Implementation")
    plt.savefig("graph.png")

#HELPER FUNCTIONS#

def isPrefix(word):
    if(word == "dr"):
        return True
    elif(word == "mr"):
        return True
    elif(word == "mrs"):
        return True
    return False

def isConstant(char):
    vowels = ["a", "e", "i", "o","u"]
    return (not char in vowels)

def getM(word):
    form = []
    ret = ""

    for i in range(len(word)):
        if(isConstant(word[i])):
            if(i != 0):
                prev = form[-1]
                if(prev != "C"):
                    form.append("C")
            else:
                form.append("C")
        else:
            if(i != 0):
                prev = form[-1]
                if(prev != "V"):
                    form.append("V")
            else:
                form.append("V")
    for char in form:
        ret = ret + char

    m = ret.count("VC")
    return m

print("STARTING TOKENIZER")
#file = "tokenization-input-part-A.txt"
file = "test.txt"
newList = (tokenization(file))
newList = (stopword(newList, "stoptest.txt"))
newList = stemming(newList)
writeTokenizedA(newList)
'''
file = "tokenization-input-part-B.txt"
newList = (tokenization(file))
newList = (stopword(newList, "stopwords.txt"))
newList = stemming(newList)
frequency(newList)
gov2(newList)
print("DONE")
'''