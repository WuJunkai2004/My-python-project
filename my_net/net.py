# !/user/bin/python
# coding=utf-8

from __future__ import print_function

__author__          ='Wu junkai ( wujunkai20041123@outlook.com )'
__version__         ='1.30.1'
__run_enviroment__  ='Python 2.6 and above'
__edit_enviroment__ ='Python 2.7.14 by python IDLE'

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

def _setup():
    ##安装模块
    def path():
        ##获取路径
        paths=sys.path[0:]
        return paths[map(len,paths).index(min(map(len,paths)))].replace('\\','/')+'/Lib/my_net.py'
    def version(paths):
        ##获取版本号
        if(os.path.exists(paths)):
            point=open(paths,'r')
            doc  =point.read()
            point.close()
            vers =re.search(r'(?<=__version__=\').+(?=\')',doc).group()
        else:
            vers='0.00.0'
        return(vers<__version__)
    def setup(paths):
        ##安装
        open(paths,'w').write(open('my_net.py','r').read())
        print('****setup successful****')
        sys.exit()
    if(version(path())):
        setup(path())

class net(object):
    ##网络处理
    def __init__(self,*url,**kw):
        if(not url):
            return
        ##数据初始化
        self.url    =url[0]
        self.data   =None
        self.file   =''
        self.host   =''
        self.path   =''
        self.headers={ 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        self.cookies=cookielib.CookieJar()
        self.handle =urllib2.HTTPCookieProcessor(self.cookies)
        self.opener =urllib2.build_opener(self.handle)
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
        if('cookie' in kw.keys()):
            self.header['Cookie']=kw['cookie']
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
            try:
                data.append(re.search(r'(?<=>).+',i).group())
            except:
                raise AttributeError('Sorry,something wrong in \' %s \''%(i))
        return data

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

    def read(self,*n):
        ##读取数据
        if(n):
            return self._text[:n[0]]
        else:
            return self._text

    def readlines():
        ##读取每行
        return self.read().split('\n')

    def readline():
        raise AttributeError('Sorry, \'readline\' has not realize .')

if(__name__=='__main__'):
    foo=net('https://www.bilibili.com/')
