# !/user/bin/python
# coding=utf-8

from __future__ import print_function

__version__='1.21.0'

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
    def __init__(self,url,**kw):
        ##数据初始化
        self.url    =url
        self.data   =None
        self.file   =''
        self.host   =''
        self.path   =''
        self.headers={ 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        self._text  =''
        self._mssg  =''
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
        except IOError:
            self._visit()
            self._save()
        else:
            if(time.time()-self.time>=172800):
                print('****over time limit****')
                self._clear()
                self._visit()
                self._save()

    def __getattr__(self,text):
        ## urllib2 的扩展与继承
        if(text in ('time','getcode','geturl','msg')):
            data=re.search(r'(?<=<%s>).+?(?=</%s>)'%(text,text),self._mssg).group()
            if(text=='time'):
                return float(data)
            else:
                return data
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
        patt=r'(?=<%s.+>).+?(?=</%s>)'%(text,text)
        get =re.findall(patt,self._text)
        data=[]
        for i in get:
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
        def message(html):
            ##生成信息
            return '<time>%s</time><getcode>%s</getcode><geturl>%s</geturl><msg>%s</msg>'%(time.time(),html.getcode(),html.geturl(),html.msg)
        ##访问网页
        requ=urllib2.Request(self.url,self.data,self.headers)
        html=urllib2.urlopen(requ)
        self._mssg=message(html)
        self._text=html.read()
        print('****read from url****')

    def _load(self):
        def line(files):
            ##读取首行
            text=''
            while(True):
                w=files.read(1)
                if(w and w!='\n'):
                    text+=w
                else:
                    return text
        ##本地加载
        if(os.path.exists('./htmls/%s/%s'%(self.path,self.file))):
            docm=open('./htmls/%s/%s'%(self.path,self.file),'r')
            self._mssg=line(docm)
            self._text=docm.read()
            docm.close()
            print('****read from file****')
        else:
            raise IOError('Sorry,cannot find ./htmls/%s/%s .'%(self.path,self.file))

    def _save(self):
        ##保存网页
        if(not os.path.exists('./htmls/%s/%s'%(self.path,self.file))):
            docm=open('./htmls/%s/%s'%(self.path,self.file),'w')
            docm.write(self._mssg+'\n')
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
        ##清除目录
        if(not os.listdir('./htmls/%s'%(self.path))):
            os.rmdir('./htmls/%s'%(self.path))
        if(not os.listdir('./htmls')):
            os.rmdir('./htmls')

    def read(self,*n):
        ##读取数据
        if(n):
            return self._text[:n[0]]
        else:
            return self._text

if(__name__=='__main__'):
    foo=net('https://www.bilibili.com/')
    foo._clear()
