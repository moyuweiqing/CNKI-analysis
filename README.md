# CNKI-analysis
###项目简介：
使用python，从知网上爬取相关的t数据，并进行数据分析，涉及到pycharm和jupyter notebook

### 研究过程：
从知网上抓取以“区块链”为主题的文献，获取文献题名、主要责任者、发表杂志、关键词、文章分类号、引用文献和被引文献等数据；对低价值数据进行清洗；数据处理；对数据结果进行可视化呈现

### 技术栈：
数据抓取：python
数据处理：python，主要涉及到jieba、networkx库
可视化：matplotlib、plotly、pyecharts

### 存储说明：
dependence存储的是依赖文件
main主要的分析部分
Results存储结果图
Jupyter notebook里面存放的是.ipynb文件，需要在Jupyter notebook下运行，主要是因为plotly库依赖Jupyter notebook环境

### 文件说明：
CNKI.py是我参考的爬虫文件
CNKI2.py是最开始用来爬取数据的爬虫文件
CNKI爬虫（改进版）是我一个师弟做的，用来分析的数据主要从这里爬取，爬取的数据存储在了知网数据.xls文件中
pdf-to-txt.py实现了从pdf到txt文件的转换
network.py封装了一部分构建网络的函数
co-citation_network.py是共被引网络分析
cooperation-network.py是作者合作网络分析
co-work_network.py是共词网络分析
keywords系列的py文件，是用不同的库进行关键词的提取，效果不同
sentiment_analysis.py是对区块链文章的情感分析
sentiment_analysis2.py是对《小王子》的情感分析
jieba_analysis.py封装了部分分词的操作函数
strategy_analysis.py战略分析，调用jieba_analysis.py构建散点图，对关键词的密度和向心度进行分析
strategy_analysis_uniform.py不调用jieba_analysis.py，直接进行分析
draw_word_cloud.py实现词云
word_cloud.py对关键词进行词云制作
Jupyter notebook里面存放的主要是要依赖Jupyter notebook开发环境的库的分析
