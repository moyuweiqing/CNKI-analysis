import pandas as pd
import jieba
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm    #字体管理，防止乱码
import math

xls = pd.ExcelFile(r'C:\Users\Yoga\Desktop\srp资料\知网-区块链(2).xls')
readf = pd.read_excel(xls, 'Sheet1')['标题']

all_word = []   #记录所有分词
dic = {}    #记录分词的出现数量

#统计所有存在的分词
for row in range(0, len(readf)):
   temp = jieba.cut(readf[row])
   for i in temp:
      if i in all_word:
         continue
      else:
         all_word.append(i)

#统计分词的出现数量
for i in all_word:
    dic[i] = 0

for row in range(0, len(readf)):
    temp = jieba.cut(readf[row])
    for i in temp:
        dic[i] = dic[i] + 1

#去除无关词
f = open(r'D:\JetBrains\PyCharm 2018.3.4\CNKI-analysis\venv\Include\dependence\stopwords.txt', encoding = "utf-8")
temp_dic = dic.copy()
f = f.read()
for i in temp_dic:
    if i in f:
        dic.pop(i)

#对分词进行排序，并挑选出出现次数最多的前20个
dic_sorted = dict(sorted(dic.items(), key = lambda x: x[1], reverse = True))
dic_20 = {}# 20个出现次数最多的词语
for i in range(0, 20):
    dic_20[list(dic_sorted.keys())[i]] = list(dic_sorted.values())[i]
print(dic_20)

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

exp_densit = []# 密度的自然对数
exp_heart = [] # 向心度的自然对数

#计算向心度
for i in dic_20.values():
    exp_densit.append(math.log(i))
for i in dic_heart.values():
    if i != 0:
        exp_heart.append(math.log(i))
    else:
        exp_heart.append(0)

#解决乱码
plt.rcParams['font.sans-serif'] =['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

plt.title(u'密度和向心度散点图')
plt.xlabel('密度的自然对数')
plt.ylabel('向心度的自然对数')

plt.scatter(exp_densit, exp_heart, s=20, c="#ff1212", marker='o')
for i in range(0, 20):
    plt.annotate(list(dic_20.keys())[i], xy = (exp_densit[i], exp_heart[i]))
plt.show()
# plt.savefig("scatter_exp.png")
