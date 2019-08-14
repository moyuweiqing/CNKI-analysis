#coding:utf-8
#author: moyuweiqing
#网络

import networkx as nx       #复杂网络分析库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 分隔关键词，并加入到列表中，去重，设置两个分隔符
# 参数说明：（frame：pd.read_excel()之后的对象，name：需要进行分析的那一列的名称，sp1、sp2为分隔符）
def seperate(frame, name, sp1, sp2):
    list = []
    for word in frame[name]:
        if sp1 in word:
            temp = word.split(sp1)
            for x in temp:
                if x not in list:
                    list.append(x)
        elif sp2 in word:
            temp = word.split(sp2)
            for x in temp:
                if x not in list:
                    list.append(x)
        else:
            if word not in list:
                list.append(word)
    return list

#填充值，存在这个关键词的dataframe的位置设置为1，其余的用0来填充
#参数说明：（frame：需要用来遍历的那个excel表格，index：用来进行遍历的frame的索引名字，name：用来进行遍历的frame的值，dataframe：用来写入的信息）
def fill(frame, index, name, dataframe):
    for row in frame[index]:  # 将这一篇文献所拥有的关键词在矩阵中标记为1
        for keyword in dataframe.columns:
            if keyword in frame.loc[row][name]:
                dataframe.loc[row][keyword] = 1
    df = dataframe.fillna(0)  # 填充空值
    return df

#检查是否有没有连接的节点
#参数说明：（list:需要进行检查的列表，x：节点，net：网络）
def check(list, x, net):
    for i in range(0,list.index(x)):
        if nx.has_path(net,x,list[i]):
            return True
    for j in range(list.index(x)+1,len(list)):
        if nx.has_path(net,x,list[j]):
            return True
    return False

#去除没有连接的节点
#参数说明：（list：需要进行检查的列表，net：网络）
def remove(list, net):
    dele = []
    for i in range(len(list)):
        if not check(list, list[i], net):
            if list[i] not in dele:
                dele.append(list[i])
    net.remove_nodes_from(dele)
    return dele, net