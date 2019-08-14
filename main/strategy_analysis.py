#coding:utf-8
#author: moyuweiqing
#战略分析，计算密度和向心度，向心度算法自己写，建立二维坐标轴

import os
import pandas as pd
import jieba_analysis
import jieba
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm    #字体管理，防止乱码
import math

path = os.path.abspath('..')
xls = pd.ExcelFile(path + '\dependence\知网数据.xls')
readf = pd.read_excel(xls, 'Sheet1')['题目'].astype(str)

#统计所有存在的分词
all_word = []   #记录所有分词
all_word = jieba_analysis.calculateAllWords(readf)

#统计分词的出现数量
dic_raw = {}    #记录分词的出现数量
dic_raw = jieba_analysis.calculateNumOfEachWord(readf, all_word)

#去除无关词
stf = open(path+'\dependence\stopwords.txt', encoding = "utf-8").read()
dic = jieba_analysis.removeIrreleventWords(stf, dic_raw)

#对分词进行排序，并挑选出出现次数最多的前20个
dic_20 = {}     #记录前20个关键词
dic_20 = jieba_analysis.sortKeyWords(dic, 20)

#建立一个空白的向心度模型
dic_heart = {}
for i in range(0, 20):
    dic_heart[list(dic_20.keys())[i]] = 0

#计算向心度
for key in dic_heart.keys():
    for row in range(0, len(readf)):
        temp = jieba.cut(readf[row])
        if key in temp:
            dic_heart[key] = dic_heart[key] + len(list(temp))

log_densit = []# 密度的自然对数
log_heart = [] # 向心度的自然对数

#计算向心度
for i in dic_20.values():
    log_densit.append(math.log(i))
for i in dic_heart.values():
    if i != 0:
        log_heart.append(math.log(i))
    else:
        log_heart.append(0)

#解决乱码
plt.rcParams['font.sans-serif'] =['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

plt.title(u'密度和向心度散点图')
plt.xlabel('密度的自然对数')
plt.ylabel('向心度的自然对数')

plt.scatter(log_densit, log_heart, s=20, c="#ff1212", marker='o')
for i in range(0, 20):
    plt.annotate(list(dic_20.keys())[i], xy = (log_densit[i], log_heart[i]))
plt.savefig(path + "\Results\scatter_log.png")