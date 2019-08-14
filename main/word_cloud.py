#coding:utf-8
#author: moyuweiqing
#词云

import os
import pandas as pd
import draw_word_cloud

if __name__ == '__main__':
   content = []
   path = os.path.abspath('..')
   xls = pd.ExcelFile(path+'\dependence\知网数据.xls') #读取数据文件
   readf = pd.read_excel(xls, 'Sheet1')  # 读取第一个表
   frame = readf[readf['题目'].notnull()]  # 如果关键词那一列非空，读取所有数据
   for keyword in frame['题目']:  # 分隔关键词，并加入到列表中，去重
      content.append(keyword)
   stopwords = open(path+'\dependence\stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
   words_dict = draw_word_cloud.statistics(content, stopwords)
   draw_word_cloud.drawWordCloud(words_dict, '区块链词云', savepath=path + '\Results')
