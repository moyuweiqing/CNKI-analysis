#coding:utf-8
#author: moyuweiqing
#共词网络可视化

import os
import networkx as nx#复杂网络分析库
import network
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = os.path.abspath('..')
xls = pd.ExcelFile(path+'\dependence\知网数据.xls')#读取xls表格
readf = pd.read_excel(xls,'Sheet1')#读取第一个表
frame = readf[readf['关键词'].notnull()]#如果关键词那一列非空，读取所有数据

keywords = network.seperate(frame, '关键词', ' ', ';')#关键词列表，里面记录了所有的关键词，没有重复
# for keyword in frame['关键词']:#分隔关键词，并加入到列表中，去重
#     if ' ' in keyword:
#         temp = keyword.split(' ')
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

#建立以标题为行，关键词为列的DataFrame矩阵
df = pd.DataFrame(index=frame['序号'],columns=keywords)
df.index.name='序号'
df.columns.name='关键词'

# for row in frame['序号']:#将这一篇文献所拥有的关键词在矩阵中标记为1
#     for keyword in df.columns:
#         if keyword in frame.loc[row]['关键词']:
#             #print(keyword)
#             df.loc[row][keyword] = 1
#
# #df为存在矩阵，dataframe类型
# #data为关联度，矩阵类型
# #df2位关联度矩阵，dataframe类型
#
# df = df.fillna(0)#填充空值
df = network.fill(frame, '序号', '关键词', df)

data = df.values.T.dot(df.values)#建立关键词之间的相关性，边的长度为相关性，在这里是将两个df点乘，df.values是按行读取值

df2 = pd.DataFrame(data = data,index=keywords,columns=keywords)#建立关键词之间的相关性矩阵

#设置阈值
valve = lambda x : x if x > 32 else 0
df2 = df2.applymap(valve)

net = nx.Graph(df2)#创建无向图，以关键词为节点，相关性为边

# def check(x,net):
#     for i in range(0,keywords.index(x)):
#         if nx.has_path(net,x,keywords[i]):
#             return True
#     for j in range(keywords.index(x)+1,len(keywords)):
#         if nx.has_path(net,x,keywords[j]):
#             return True
#     return False
#
# #去除无连接节点
# dele=[]
# for i in range(len(keywords)):
#     if not check(keywords[i],net):
#         if keywords[i] not in dele:
#             dele.append(keywords[i])
# net.remove_nodes_from(dele)
dele, net = network.remove(keywords, net)

de=dict(net.degree())#建立字典，关键字为索引，度（关联情况）为值
pos = nx.spring_layout(net)#四种建图模式，spectral,shell,circular,spring，spring是可以看的了
keywords = [i for i in keywords if i not in dele]#有边的关键词

array = np.zeros(len(keywords))#建立以度为值的一维矩阵
arg = np.argsort(-np.array(array))
labels = {}#记录关键词
for index in range(0, len(keywords)):
    labels[keywords[arg[index]]] = keywords[arg[index]]

de2 = [de[v]*60 for v in sorted(de.keys(), reverse=False)]#应该是节点的大小，尺寸调整合适

plt.figure(figsize=(50, 50))
nx.draw_networkx_labels(net,pos,labels, font_size=40,font_color='black',font_family ='YouYuan')
nx.draw_networkx(net, pos, node_size=de2, with_labels = False, node_color='#A52A2A', linewidths=None, width=2.0, edge_color ='#858585')