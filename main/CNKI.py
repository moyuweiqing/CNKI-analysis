#初始的爬虫案例，主要参照于这个来做
#coding:utf-8

import requests
from bs4 import BeautifulSoup as bs
import time
import xlwt
import openpyxl
import re


def pagenext():
    base_url = 'http://search.cnki.com.cn/search.aspx?q=%E6%96%B0%E9%97%BB%E4%BC%A0%E6%92%AD&rank=relevant&cluster=Type&val=I141&p='
    L = range(0, 840)  # 最尾巴的数不计入
    All_Page = []
    for i in L[::10]:
        next_url = base_url + str(i)
        # print(next_url)
        print("第 ", i / 10 + 1, " 页的数据")
        page_text = spider(next_url)
        time.sleep(10)
        for page in page_text:
            All_Page.append(page)
    print(All_Page)
    write_excel('xlsx论文筛选.xlsx', 'info', All_Page)


def datespider(date_url):
    # 因为跳转的链接类型不一样，所以我们要判断这两种链接是哪一种并且选择不一样的解析find方法
    response_try = requests.get(date_url, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'})
    # print(response_try.text)
    response_tree = bs(response_try.text, 'html.parser')
    # 根据两个不同的链接返回不一样的值
    if re.match(r'http://www.cnki.com.cn/Article/[0-9a-zA-Z\_]+', date_url):
        res_date = response_tree.find("font", {"color": "#0080ff"})
        if res_date == None:
            response_date = None
        else:
            response_date = res_date.get_text().replace('\r', '').replace('\n', '')
    else:
        response_date = response_tree.find("title").get_text()[-8:]
    return response_date


def write_excel(path, sheet_name, text_info):
    index = len(text_info)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        for j in range(len(text_info[i])):
            sheet.cell(row=i + 1, column=j + 1, value=str(text_info[i][j]))
    workbook.save(path)
    print("xlsx格式表格写入数据成功！")


def spider(url):
    response = requests.get(url, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'})
    res = response.content
    html = str(res, 'utf-8')
    html_tree = bs(html, 'lxml')
    # 找打h3标签下的内容
    html_text = html_tree.find_all("h3")
    All_text = []
    # 隔一个才是文章的标题
    for text in html_text[1:-2:]:
        one_text = []
        text_title = text.get_text().replace('\xa0', '').replace('\n', '')  # 得到论文的标题
        # print(text.get_text())
        text_url = text.find('a')['href']  # 选取了当前文章的链接
        # 用正则表达式匹配我们需要的链接
        if re.match(r"""http://youxian.cnki.com.cn/yxdetail.aspx\?filename=[0-9a-zA-Z]+&dbname=[a-zA-Z]+""",
                    text_url) or re.match(r'http://www.cnki.com.cn/Article/[a-zA-Z]+-[0-9a-zA-Z-]+.htm', text_url):
            # print(text.find('a')['href'])
            text_date = datespider(text_url)
            one_text.append(text.get_text().replace('\xa0', '').replace('\n', ''))  # text.get_text是得到文章的标题
            if text_date == None:
                one_text.append(None)
            else:
                if int(text_date[:4]) >= 2014:
                    one_text.append(text_date.replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', ''))
                else:
                    continue
            All_text.append(one_text)
    # print(text.find('a')['href'])

    # print(All_text)
    return All_text


# write_excel(All_text)


if __name__ == '__main__':
    pagenext()