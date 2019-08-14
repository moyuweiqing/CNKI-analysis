#coding:utf-8
#author: moyuweiqing
#合作网络可视化

import os
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  #导入所需要的库

path = os.path.abspath('..')
xlsx = pd.ExcelFile(path+'\dependence\知网数据.xls') #读取数据文件
readf = pd.read_excel(xlsx,'Sheet1')

#数据进行预处理，将读入的作者以及相关作者信息转换为列表形式
for i in range(len(readf['作者'])):
    if readf['作者'][i] != '[]':
        readf['作者'][i] = eval(readf['作者'][i])
    else:
        readf['作者'][i] = np.nan
for j in range(len(readf['相关作者'])):
    if readf['相关作者'][j] is not np.nan:
        readf['相关作者'][j] = eval(readf['相关作者'][j])

#数据预处理，将作者为空的数据去除
frame = readf[readf['作者'].notnull()]
frame.index = frame['题目']

#获取作者以及相关作者，将其整合到一个列表中
all_authors = []
for authors in frame['作者']:
    for author in authors:
        if author not in all_authors:
            all_authors.append(author)
for r_authors in frame['相关作者']:
    if r_authors is not np.nan:
        for r_author in r_authors:
            if r_author not in all_authors:
                all_authors.append(r_author)

#构建出现矩阵
df = pd.DataFrame(index=frame['题目'],columns=all_authors)
df.index.name='题目'
df.columns.name='作者'
for title in frame['题目']:
    for i in frame.loc[title]['作者']:
        df.loc[title,i] = 1
    if frame.loc[title]['相关作者'] is not np.nan:
        for j in frame.loc[title]['相关作者']:
            df.loc[title,j] = 1
df=df.fillna(0)

#将出现矩阵转换为共现矩阵
data = df.values.T.dot(df.values)
df2 = pd.DataFrame(data = data,index=all_authors,columns=all_authors)

#设置阀门，排除关联度小的点
valve = lambda x : x if x > 32 else 0
df2 = df2.applymap(valve)

#构建共现网络
net = nx.Graph(df2)

#过滤关联度为0的节点
def check(x,net):
    for i in range(0,all_authors.index(x)):
        if nx.has_path(net,x,all_authors[i]):
            return True
    for j in range(all_authors.index(x)+1,len(all_authors)):
        if nx.has_path(net,x,all_authors[j]):
            return True
    return False
dele=[]
for i in range(len(all_authors)):
    if not check(all_authors[i],net):
        if all_authors[i] not in dele:
            dele.append(all_authors[i])
net.remove_nodes_from(dele)

#设置每个节点的大小比例为它们度的大小比例，并且显示每个节点的标签
de=dict(net.degree())
pos = nx.spring_layout(net)
all_authors = [i for i in all_authors if i not in dele]
array = np.zeros(len(all_authors))
j = 0
for i in de.keys():
    array[j] = de[i]
    j+=1
arg = np.argsort(-np.array(array))
labels = {}
for index in range(len(all_authors)):
    labels[all_authors[arg[index]]] = all_authors[arg[index]]
de2 = [de[v]*20 for v in sorted(de.keys(), reverse=False)]

#对网路进行可视化
plt.figure(figsize=(50, 50))
nx.draw_networkx_labels(net,pos,labels, font_size=40,font_color='black',font_family ='YouYuan')
nx.draw_networkx(net, pos, node_size=de2, with_labels = False, node_color='#A52A2A', linewidths=None, width=1.0, edge_color ='#858585')
