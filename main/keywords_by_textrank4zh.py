#coding:utf-8
#author: moyuweiqing
#使用textrank4zh来进行关键词的提取

import os
from textrank4zh import TextRank4Keyword

path = os.path.abspath('..')
text = open(path+'\dependence\区块链技术发展现状与展望_袁勇.txt').read().replace('\n', '').replace(' ', '')

tr4w = TextRank4Keyword()
tr4w.analyze(text, lower=True)
key_words = tr4w.get_keywords(20)
# print(key_words)
word_list = list(key_word.word for key_word in key_words)

stopwords = {}.fromkeys([ line.rstrip() for line in open(path+'\dependence\stopwords.txt', encoding = "utf-8") ])
final = ""
for word in word_list:
    if word not in stopwords:
        if (word != "。" and word != "，") :
            final = final + " " + word

print(final)