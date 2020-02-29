# -*- coding: utf-8 -*-

from collections import deque
import itertools
grammer = [{'S':"NP VP"},
           {"NP":"ART N"},{"NP":"NP PP"},{"NP":"PRON"},{"NP":"N"},
           {"VP":"VP PP"},{"VP":"V NP"},
           {"PP":"P NP"},{"ART":"a"},{"ART":"an"},{"ART":"the"},
           {"N":"boy"},{"N":"telescope"},{"N":"football"},{"N":"jam"},{"N":"book"},{"N":"saw"},{"N":"play"},
            {"PRON":"I"},{"PRON":"we"},{"PRON":"you"},{"PRON":"they"},
            {"V":"saw"},{"V":"play"},{"V":"eat"},{"V":"study"},{"V":"jam"},
            {"P":"with"},{"P":"for"}]

def print_table(table):
    for i in table:
        print(i[1:])

def match_index(strr ,list_values):
    index = []
    i=0
    for ind in list_values:
        if(ind==strr):
            index.append(i)
        i += 1
    return index

def match_list_index(list1,list2,dict_values):
    index = []
    for i1 in list1:
        for i2 in list2:
            temp = i1+" "+i2
            i=0
            for i3 in dict_values:
                if(i3==temp):
                    index.append(i)
                i += 1

    return index

def match_list_grammer(list1,list2,list21,list22,dict_values):
    index2 = []
    for i1,j1 in zip(list1,list21):
        for i2,j2 in zip(list2,list22):
            temp = i1+" "+i2
            i=0
            for i3 in dict_values:
                if(i3==temp):
                    temp2 = str(" ".join(grammer[i].keys()))+str(j1) + " " + str(j2)
                    index2.append(temp2)
                i+=1
    return index2

def cyk_parse(words, grammer, n_words):
    # table = np.array(n_words*n_words)
    # table = [[0] * n_words] * n_words
    print("################################## BOTTOM_UP CKY PARSING TECHNIQUE###################################################")
    table = [[list('0') for i in range(n_words+1)] for j in range(n_words)]
    table2 = [[list('0') for i in range(n_words + 1)] for j in range(n_words)]


##########################################################################
    # for getting list of values of grammer
    list_value=[]
    # iterate over list of dict
    for i in grammer:
        list_value += i.values()

##########################################################################

    for j in range(1,n_words+1):
        try :
            indexs = match_index(words[j-1],list_value)
            temp = []
            temp_t2=[]
            itt_v ="s"
            for idx in indexs:
                temp.append(''.join(grammer[idx].keys()))
                temp_t2.append(str(grammer[idx]))
                itt_v = grammer[idx]
                i_temp = match_index(''.join(grammer[idx].keys()),list_value)

                if(len(i_temp)>0):
                    for idx2 in i_temp:
                        temp.append(''.join(grammer[idx2].keys()))
                        temp_t2.append("("+" ".join(grammer[idx2].keys())+"("+str(itt_v)+")"+")")
            table[j-1][j]=temp
            table2[j -1][j] = temp_t2
        except:
            print("ERROR")
        for i in range(j-2,-1,-1):
            temp = []
            temp2= []
            for k in range(i+1,j):
                if(table[i][k]=='0' or table[k][j]=='0'):
                    table[i][j]=list('0')
                    continue
                else:
                    ix1= match_list_index(table[i][k],table[k][j],list_value)
                    tx1 = match_list_grammer(table[i][k],table[k][j],table2[i][k], table2[k][j], list_value)
                    if(len(tx1)>0):
                        temp2.append(tx1)
                    for idx in ix1:
                        temp.append(''.join(grammer[idx].keys()))
                    table[i][j] = temp
                    table2[i][j]=temp2
    if('S' in table[0][n_words]):
        print("------CKY PARSING TABLE------")
        print_table(table)
        print("------PARSING POSSIBLE------")
        print()
        for it1 in table2[0][n_words]:
            t1=1;
            for it2 in it1:
                il = it2.replace("\\", " ")
                il = il.replace(" ","")
                il = il.replace("[","(")
                il = il.replace("]", ")")
                il = il.replace("{", "(")
                il = il.replace("}", ")")
                il = il.replace("'", " ")
                il = il.replace("\"", " ")
                print("PARSE TREE",t1,":(",il+")")
                t1+=1
    else:
        print("------CKY PARSING TABLE------")
        print()
        print_table(table)
        print("------PARSING NOT POSSIBLE------")
    print("##################################PARSING DONE###################################################")
    print()

sentence = [
    "I saw a boy with a telescope" \
    , "we play football" \
    , "they eat the jam" \
    , "I play with you"
    , "you saw a play"
]

############################TESTING SENTENCES##################################################
'''
( S ( NP ( PRON “I” ) ) ( VP ( V “saw” ) ( NP ( ART “a”) ( N “boy”)) ( PP ( P “with”) ( NP (
ART “a” ) ( N “telescope”)))))
( S ( NP ( PRON “I” ) ) ( VP ( V “saw” ) ( NP ( ART “a”) ( N “boy”) ( PP ( P “with”) ( NP ( ART
“a” ) ( N “telescope”))))))
'''
for t in sentence:
    # if t == sentence[4]:
    print("PARSING SENTENCE:", t)
    cyk_parse(t.rsplit(), grammer, len(t.rsplit()))
################################################################################################

