#coding:utf-8
#author: moyuweiqing
#使用jieba库进行分词、统计词频、去除无关词

import jieba

#统计所有存在的分词
def calculateAllWords(readfile):
    all_word = []   #记录所有分词
    for row in range(0, len(readfile)):
        temp = jieba.cut(readfile[row])
        for i in temp:
            if i in all_word:
                continue
            else:
                all_word.append(i)
    #all_word.pop()
    return all_word

#统计分词的出现数量
def calculateNumOfEachWord(readfile, all_word):
    dic = {}  # 记录分词的出现数量
    for i in all_word:
        dic[i] = 0
    for row in range(0, len(readfile)):
        temp = jieba.cut(readfile[row])
        for i in temp:
            dic[i] = dic[i] + 1
    return dic

# 去除无关词
def removeIrreleventWords(stopwords, dic):
    temp_dic = dic.copy()
    for i in temp_dic:
        if i in stopwords:
            dic.pop(i)
    return dic

#对关键词进行排序
def sortKeyWords(keyword,num):
    dic_sorted = dict(sorted(keyword.items(), key=lambda x: x[1], reverse=True))
    dic_num = {}
    for i in range(0, num):
        dic_num[list(dic_sorted.keys())[i]] = list(dic_sorted.values())[i]
    return dic_num