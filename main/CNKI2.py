#coding:utf-8
#author: moyuweiqing
#主爬虫，数据用这个来爬取的

#爬虫须知：
#  1、运行前请配置包 requests、bs4、xlutils、my_fake_useragent
#  2、Excel 文件请先在同一级目录新建好，代码里的名字：知网-区块链.xls（不能是xlsx后缀）
#  3、目前测试 只能爬取18页的数据，到19页就会失败，好像有个上限，没想到它是怎么识别的


import requests #爬取IP端口和
from bs4 import BeautifulSoup as bs #bs4解析库，用来解析网页
import time
import openpyxl #对Excel的操作
import re   #对字符串的操作
import xlrd #xls文件的读
import xlwt #xls文件的写
from xlutils.copy import copy#修改（追加写入）
from my_fake_useragent import UserAgent #这个库用来做反爬虫的
#这库用来随机生成user_agent 在这个爬虫中好像没必要 一样会循环重定向

def pagenext():
    #最开始的链接 最后面 'p=' 添加你要的页数 就能去其他页
    base_url = 'http://search.cnki.com.cn/Search.aspx?q=%e5%8c%ba%e5%9d%97%e9%93%be&rank=relevant&cluster=all&val=&p='
    L = range(0, 450) #修改这里可以改变获取的数量 不要太多 不然跑很久    4500就是300页了
    # All_Page = []
    for i in L[::15]: #15条是一页
        All_Page = []
        next_url = base_url + str(i)#配置下一页的url，每15个数据一页
        print(next_url)
        print(i / 15 + 1, " 页的数据")
        page_text = spider(next_url)      #跑第*页的爬虫 获取那一页的数据
        time.sleep(10)        #休息一会 防被网站 ban
        write_excel('xlsx论文筛选.xls',i / 15 + 1, page_text)  #写进Excel

#进入了文章的具体ulr
def datespider(date_url):
    #设置一下 UserAgent 突破反扒
    response_try = requests.get(date_url, UserAgent().random())
    # 用BeautifulSoup框架转化
    response_tree = bs(response_try.text, 'html.parser')
    if(response_tree==None):
        return []
    else:
        # 在对应位置 匹配需要的信息
        res_date = response_tree.find("font", {"color": "#0080ff"})
        res_name = response_tree.find("div", {"style": "text-align:center; width:740px; height:30px;"})
        res_msg = response_tree.find("div", {"style": "text-align:left;"})

        #时间
        if res_date == None:
            response_date = None
        else:
            response_date = res_date.get_text().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\t', '')
        #作者
        if res_name == None:
            response_name = None
        else:
            response_name = res_name.get_text().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\t', '')
        #其他信息
        if res_msg == None:
            res_msg = None
        else:
            # 去除不想要的东西
            response_msg = res_msg.get_text().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\t','')\
                .replace('】', '').replace('学位授予单位：', '').replace('学位级别：', '').replace('作者单位：', '').replace('学位授予年份：','').replace('分类号：', '')
            #用“【”作为分割界限，将response_msg字符串 划分为 response_point列表
            response_point = response_msg.split("【")
        #插入列表 并返回
        response_All = []
        response_All.append(response_date)
        response_All.append(response_name)
        #列表拼接
        #列表拼接
        for item in range(1,len(response_point)):
            response_All.append(response_point[item])

        return response_All

#写进表格里面去
def write_excel(path, page, text_info):

    index = len(text_info)
    # workbook = openpyxl.Workbook()
    workbook = xlrd.open_workbook(path)#打开
    sheets = workbook.sheet_names()
    sheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = sheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    # sheet.title = sheet_name
    for i in range(0, index):
        for j in range(len(text_info[i])):
            new_worksheet.write(i + rows_old,j,str(text_info[i][j]))
    new_workbook.save(path)

    print(page," 页写入数据成功！")

def spider(url):
    response = requests.get(url, {'User-Agent':UserAgent().random()})#用来突破反爬虫
    res = response.content
    html = str(res, 'utf-8')#用来获取html页面
    html_tree = bs(html, 'lxml')
    # 找class = wz_content标签下的内容
    html_text = html_tree.find_all("div", class_="wz_content")
    All_text = []
    for text in html_text:
        one_text = []
        text_url = text.find('a')['href']  # 选取了当前文章的链接
        text_title = text.find('h3') #标题
        text_cout = text.find("span", class_="count")
        #舍弃http://youxian.cnki链接 打不开的 没数据 可能需要登陆才有数据 之后再调试吧  出现概率1/20
        if re.match(r'http://www.cnki.com.cn/Article/[a-zA-Z]+-[0-9a-zA-Z-]+.htm', text_url) or re.match(r'http://cdmd.cnki.com.cn/Article/[a-zA-Z]+-[0-9a-zA-Z-]+.htm', text_url):
            # 调用函数 进去各个文章的具体网站 找其他信息
            text_all = datespider(text_url)
            one_text.append(text_title.get_text().replace('\xa0', '').replace('\n', ''))  # 得到文章的标题
            one_text.append(text_cout.get_text().replace('\xa0', '').replace('\n', '').replace('下载次数', '').replace('被引次数', '').replace('（', '').replace('）', ''))  # 把操作次数 放进列表
            for item in text_all:#将datespider函数返回的信息，文章的 作者、单位、学位 、分类号，插入列表
                one_text.append(item.replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', '').replace('年', ''))
            one_text.append(text_url)  # 把文章的链接 放进列表

            All_text.append(one_text)
    return All_text

if __name__ == '__main__':
    pagenext()