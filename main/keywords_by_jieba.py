#coding:utf-8
#author: moyuweiqing
#使用jieba库来进行关键词的提取

import os
import jieba
import jieba.analyse

path = os.path.abspath('..')
text = open(path + '\dependence\区块链技术发展现状与展望_袁勇.txt')
text = text.read()
s1 = text.replace('\n', '').replace(' ', '')#去除换行

fenci_text = jieba.cut(s1)
stopwords = {}.fromkeys([ line.rstrip() for line in open(path + '\dependence\stopwords.txt', encoding = "utf-8") ])
final = ""
for word in fenci_text:
    if word not in stopwords:
        if (word != "。" and word != "，") :
            final = final + " " + word

keywords = jieba.analyse.extract_tags(final, topK = 20, withWeight = True, allowPOS = ())
print(keywords)