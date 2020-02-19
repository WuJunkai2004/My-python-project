# !/user/bin/env python
# coding=utf-8

from __future__ import print_function

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib
import urllib
import time
import sys
import os
import re

if(__name__=='__main__'):
    __file__        =os.path.basename(sys.argv[0])
else:
    __file__        ='%s.py'%(__name__)
__author__          ='Wu junkai ( wujunkai20041123@outlook.com )'
__version__         ='1.42.0'
__run_enviroment__  ='Python 2.6 and above'
__edit_enviroment__ ='Python 2.7.14 by python IDLE'

def _setup():
    ##安装模块
    def path():
        ##获取路径
        return "%s\\Lib\\%s"%(sys.path[map(os.path.exists,map(''.join,zip(sys.path,['\\python.exe']*len(sys.path)))).index(True)],__file__)
    def version():
        ##获取版本号
        if(os.path.exists(path())):
            point=open(path(),'r')
            doc  =point.read()
            point.close()
            vers =re.search(r'(?<=__version__).+',doc).group()
            vers =re.search(r'(?<=\').+?(?=\')',vers).group()
        else:
            vers='0.00.0'
        return(vers<__version__)
    def setup():
        ##安装
        open(path(),'w').write(open(__file__,'r').read())
        print('****setup successful****')
        sys.exit()
    if(version()):
        setup()

def _header():
    ##管理 headers
    return {
        'Accept-Language'   : 'zh-CN,zh;q=0.9,en;q=0.8' ,
        'User-Agent'        : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }


class web(object):
    ##网页处理
    def __init__(self,string=''):
        ##初始化
        self._text=string
        self.__pos__=0

    def __getattr(self,text):
        return self._tag(text)

    def _tag(self,text):
        ##标签查找
        patt=r'(?=<%s.+>).+?(?=</%s>)'%(text,text)
        get =re.findall(patt,self._text)
        data=[]
        for i in get:
            if(re.search(r'(?<=>).+',i)):
                data.append(re.search(r'(?<=>).+',i).group())
        return data

    def read(self,*n):
        ##读取数据
        if(n):
            self.__pos__+=n[0]
            return self._text[self.__pos__-n[0]:n[0]]
        else:
            return self._text[self.__pos__:]

    def readlines(self):
        ##读取每行
        return self.read().split('\n')

    def readline(self):
        ##仅读取一行
        text=''
        while(self.__pos__<len(self._text) and self._text[self.__pos__]!='\n'):
            text+=self._text[self.__pos__]
            self.__pos__+=1
        self.__pos__+=1
        return text

    def tell(self):
        ##返回指针位置
        return self.__pos__

    def seek(self,*n):
        ##重置指针
        if(n):
            if(n[0]>=len(self._text)):
               raise BaseException('A length error : your file is not long enough')
            else:
               self.__pos__=n[0]
        else:
               self.__pos__=0


class net(web):
    ##网络处理
    def __init__(self,url='',**kw):
        ##数据初始化
        super(net,self).__init__()
        self.url    =url
        self.data   =None
        self.file   =''
        self.host   =''
        self.path   =''
        self.headers=_header()
        self.cookies=cookielib.CookieJar()
        self.handle =urllib2.HTTPCookieProcessor(self.cookies)
        self.opener =urllib2.build_opener(self.handle)
        self._mssg  =''
        ##获取传入数据
        if('headers' in kw.keys()):
            self.headers=kw['headers']
        if('data'    in kw.keys()):
            self.data=urllib.urlencode(kw['data'])
        if('cookie'  in kw.keys()):
            self.headers['Cookie']=kw['cookie']
        if('host'    in kw.keys()):
            self.headers['Host']=kw['host']
        if(self._analyze()):
            ##处理网络数据
            try:
                self._load()
            except IOError:
                self._visit()
                self._save()
            else:
                ##超时处理
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
            except BaseException:
                return data[0]
        elif(len(data)==0):
            raise AttributeError('Sorry,cannot find %s'%(text))
        else:
            return data

    def _analyze(self):
        if(not self.url):
            return False
        ##校准并解析 url
        if(self.url[-1]!='/'):
            self.url+='/'
        self.host =re.search(r'(?<=//).+?(?=/)',self.url).group()
        self.path =self._named(self.host)
        try:
            if(self.url.split('.')[-1] not in ('html/','htm/')):
                self.file =self._named(re.search(r'(?<=%s/).+(?=/)'%(self.host),self.url).group())+'.html'
            else:
                self.file =self._named(re.search(r'(?<=%s/).+(?=/)'%(self.host),self.url).group())
                self.file =re.sub(r'_htm',r'.htm',self.file)
        except AttributeError:
            self.file ='home.html'
        ##补充 host
        if('Host' not in self.headers.keys()):
            self.headers['Host']=self.host
        return True

    def _named(self,text):
        ##转化特殊字符
        return re.sub(r'[\W]','_',text)

    def _visit(self):
        ##访问网页
        requ=urllib2.Request(self.url,self.data,self.headers)
        html=self.opener.open(requ)
        self._mssg='<time>%s</time><getcode>%s</getcode><geturl>%s</geturl><msg>%s</msg>'%(time.time(),html.getcode(),html.geturl(),html.msg)
        self._text=html.read()
        print('****read from url****')

    def _load(self):
        ##本地加载
        if(os.path.exists('./htmls/%s/%s'%(self.path,self.file))):
            docm=open('./htmls/%s/%s'%(self.path,self.file),'r')
            self._mssg=docm.readline()[:-1]
            self._text=docm.read()
            docm.close()
            print('****read from file****')
        else:
            raise IOError('Sorry,cannot find ./htmls/%s/%s .'%(self.path,self.file))

    def _save(self):
        ##创建目录
        if(not os.path.exists('./htmls')):
            os.mkdir('htmls')
        if(not os.path.exists('./htmls/%s'%(self._named(self.host)))):
            os.mkdir('./htmls/%s'%self._named(self.host))
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
