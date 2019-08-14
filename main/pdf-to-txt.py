#coding:utf-8
#author: moyuweiqing
#pdf转换成txt

import time,os.path,requests,re
time1=time.time()
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams,LTTextBoxHorizontal
from pdfminer.pdfpage import PDFTextExtractionNotAllowed,PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


class CPdf2TxtManager():
    def changePdfToText(self, filePath):
        # 以二进制读模式打开
        file = open(path, 'rb')
        #用文件对象来创建一个pdf文档分析器
        praser = PDFParser(file)
        # 创建一个PDF文档对象存储文档结构,提供密码初始化，没有就不用传该参数
        doc = PDFDocument(praser, password='')
        ##检查文件是否允许文本提取
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed

        # 创建PDf 资源管理器 来管理共享资源，#caching = False不缓存
        rsrcmgr = PDFResourceManager(caching = False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        # 创建一个PDF页面聚合对象
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解析器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 获得文档的目录（纲要）,文档没有纲要会报错
        #PDF文档没有目录时会报：raise PDFNoOutlines  pdfminer.pdfdocument.PDFNoOutlines
        # print(doc.get_outlines())

        # 获取page列表
        print(PDFPage.get_pages(doc))
        # 循环遍历列表，每次处理一个page的内容
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            for x in layout:
                if hasattr(x, "get_text"):
                    fileNames = os.path.splitext(filePath)
                    with open(fileNames[0] + '.txt','a+') as f:
                        results = x.get_text()
                        print(results)
                        f.write(results.encode('gbk','ignore').decode('gbk') + '\n')
                # 如果x是水平文本对象的话
                # if (isinstance(x, LTTextBoxHorizontal)):
                #     text = re.sub(replace, '', x.get_text())
                #     if len(text) != 0:
                #         print(text)

if __name__ == '__main__':
    path = os.path.abspath('..')
    pdf2TxtManager = CPdf2TxtManager()
    pdf2TxtManager.changePdfToText(path+'\dependence\区块链技术发展现状与展望_袁勇.pdf')
    time2 = time.time()
    print('ok,解析pdf结束!')
    print('总共耗时：' + str(time2 - time1) + 's')