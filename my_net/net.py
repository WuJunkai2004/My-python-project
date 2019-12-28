# !/user/bin/python
# coding=utf-8

from __future__ import print_function

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
import urllib
import time
import os
import re

class net(object):
    ##网络处理
    ##version 1.00.0
    def __init__(self,url,**kw):
        ##数据初始化
        self.url    =url
        self.data   =None
        self.file   =''
        self.host   =''
        self.path   =''
        self.headers={ 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        self._text  =''
        ##校准 url
        if(self.url[-1]!='/'):
            self.url+='/'
        ##获取传入数据
        if('headers' in kw.keys()):
            self.headers=kw['headers']
        if('data' in kw.keys()):
            self.data=urllib.urlencode(kw['data'])
        ##解析 url
        self.host =re.search(r'(?<=//).+?(?=/)',self.url).group()
        self.path =self._named(self.host)
        try:
            self.file =self._named(re.search(r'(?<=%s/).+(?=/)'%(self.host),self.url).group())+'.html'
        except AttributeError:
            self.file ='home.html'
        ##补充 host
        if('Host' not in self.headers.keys()):
            self.headers['Host']=self.host
        ##处理网络数据
        self._create()
        try:
            self._load()
        except:
            self._visit()
            self._save()
        else:
            pass
    def __getattr__(self,text):
        ##快捷的标签查找
        data=self._tag(text)
        if(len(data)==1):
            try:
                return eval(data[0])
            except:
                return data[0]
        elif(len(data)==0):
            raise AttributeError('Sorry,cannot find %s'%(text))
        else:
            return data
    def _tag(self,text):
        ##标签查找
        patt=r'(?=<%s[\w\W]{0,}>).+?(?=</%s>)'%(text,text)
        get =re.findall(patt,self._text)
        data=[]
        for i in get:
            if(re.search(r'(?<=>).+',i)):
                data.append(re.search(r'(?<=>).+',i).group())
        return data
    def _named(self,text):
        ##转化特殊字符
        return re.sub(r'[\W]','_',text)
    def _create(self):
        ##创建目录
        if(not os.path.exists('./htmls')):
            os.mkdir('htmls')
        if(not os.path.exists('./htmls/%s'%(self._named(self.host)))):
            os.mkdir('./htmls/%s'%self._named(self.host))
    def _visit(self):
        ##访问网页
        requ=urllib2.Request(self.url,self.data,self.headers)
        html=urllib2.urlopen(requ)
        self._text=html.read()
        print('****read from url****')
    def _load(self):
        ##本地加载
        if(os.path.exists('./htmls/%s/%s'%(self.path,self.file))):
            docm=open('./htmls/%s/%s'%(self.path,self.file),'r')
            self._text=docm.read()
            docm.close()
            print('****read from file****')
        else:
            raise IOError('Sorry,cannot find ./htmls/%s/%s .'%(self.path,self.file))
    def _save(self):
        ##保存网页
        if(not os.path.exists('./htmls/%s/%s'%(self.path,self.file))):
            docm=open('./htmls/%s/%s'%(self.path,self.file),'w')
            docm.write(self._text)
            docm.close()
        else:
            raise IOError('Sorry, ./htmls/%s/%s already exists .'%(self.path,self.file))
    def _clear(self):
        ##删除网页
        if(os.path.exists('./htmls/%s/%s'%(self.path,self.file))):
            os.remove('./htmls/%s/%s'%(self.path,self.file))
        else:
            raise IOError('Sorry, ./htmls/%s/%s does not exists .'%(self.path,self.file))
    
if(__name__=='__main__'):
    foo=net('https://www.runoob.com/python/python-exceptions.html')
    print(foo.title)
    foo._clear()
