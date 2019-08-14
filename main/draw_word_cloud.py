#coding:utf-8
#author: moyuweiqing
#使用wordcloud库画词云

import os
import jieba
import imageio as ima	#读入图片文件
from wordcloud import WordCloud

def drawWordCloud(words, title, savepath='./results'): #定义一个词云绘制函数，通过词频绘制词云图并写出到特定目录
   path = os.path.abspath('..')
   if not os.path.exists(savepath):
      os.mkdir(savepath)
   wc = WordCloud(font_path=path+'\dependence\simkai.ttf', background_color='white', max_words=2000, width=1920, height=1080, margin=5, mask=ima.imread(path+'\dependence\mask.png'))#使用原先准备好的一张照片作为背景图
   wc.generate_from_frequencies(words)
   wc.to_file(os.path.join(savepath, title+'.png'))

def statistics(texts, stopwords):  #使用jieba库来进行分词，并统计词语出现次数
   words_dict = {}
   for text in texts:
      temp = jieba.cut(text)
      for t in temp:
         if t in stopwords:
            continue
         if t in words_dict.keys():
            words_dict[t] += 1
         else:
            words_dict[t] = 1
   return words_dict