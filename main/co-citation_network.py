#coding:utf-8
#author: moyuweiqing
#共引文献网络分析，和共词网络分析差不多

import os
import networkx as nx#复杂网络分析库
import network
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = os.path.abspath('..')
xls = pd.ExcelFile(path+'\dependence\知网数据.xls')#读取xls表格
readf = pd.read_excel(xls,'Sheet1')#读取第一个表
frame = readf[readf['共引文献'].notnull()]#如果关键词那一列非空，读取所有数据

keywords = network.seperate(frame, '共引文献', ' ', ';')#关键词列表，里面记录了所有的关键词，没有重复
# for keyword in frame['共引文献']:#分隔关键词，并加入到列表中，去重
#     if ',' in keyword:
#         temp = keyword.split(',')
#         for x in temp:
#             if x not in keywords:
#                 keywords.append(x)
#     elif ';' in keyword:
#         temp = keyword.split(';')
#         for x in temp:
#             if x not in keywords:
#                 keywords.append(x)
#     else:
#         if keyword not in keywords:
#             keywords.append(keyword)

df = pd.DataFrame(index=frame['序号'],columns=keywords)    #建立以标题为行，关键词为列的DataFrame矩阵
df.index.name='序号'
df.columns.name='共引文献'
#
# #将这一篇文献所拥有的关键词在矩阵中标记为1
# for row in frame['序号']:
#     for keyword in df.columns:
#         if keyword in frame.loc[row]['共引文献']:
#             df.loc[row][keyword] = 1
# df = df.fillna(0)#填充空值

df = network.fill(frame, '序号', '共引文献', df)

#df为存在矩阵，dataframe类型
#data为关联度，矩阵类型
#df2位关联度矩阵，dataframe类型

data = df.values.T.dot(df.values)#建立关键词之间的相关性，边的长度为相关性，在这里是将两个df点乘，df.values是按行读取值
df2 = pd.DataFrame(data = data,index=keywords,columns=keywords)#建立关键词之间的相关性矩阵，以关联度作为值传入

#设置阈值
value = lambda x : x * 30 if x > 0 else 0
df2 = df2.applymap(value)

net = nx.Graph(df2)#创建无向图，以关键词为节点，相关性为边

dele, net = network.remove(keywords, net)

de=dict(net.degree())#建立字典，关键字为索引，度（关联情况）为值
pos = nx.spring_layout(net)#四种建图模式，spectral,shell,circular,spring，spring是可以看的了

array = np.zeros(len(keywords))#建立以度为值的一维矩阵
arg = np.argsort(-np.array(array))
labels = {}#记录关键词
for index in range(0, len(keywords)):
    labels[keywords[arg[index]]] = keywords[arg[index]]

de2 = [de[v]*10 for v in sorted(de.keys(), reverse=False)]#应该是节点的大小，尺寸调整合适

plt.figure(figsize=(50, 50))
nx.draw_networkx_labels(net,pos,labels, font_size=40,font_color='black',font_family ='YouYuan')#写标记
nx.draw_networkx(net, pos, node_size=de2, with_labels = False, node_color='#A52A2A', linewidths=None, width=2.0, edge_color ='#858585')