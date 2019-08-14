#coding:utf-8
#author: moyuweiqing
#使用SnowNlp来提取关键词

import os
from snownlp import SnowNLP

path = os.path.abspath('..')
text = open(path + '\dependence\区块链技术发展现状与展望_袁勇.txt').read().replace('\n', '').replace(' ', '')

analysis_result = SnowNLP(text)
stopwords = {}.fromkeys([ line.rstrip() for line in open(path + '\dependence\stopwords.txt', encoding = "utf-8") ])
final = ""
for word in analysis_result.keywords(20):
    if word not in stopwords:
        if (word != "。" and word != "，") :
            final = final + " " + word

print(final)