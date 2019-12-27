# !/user/bin/python
# coding=utf-8

from __future__ import print_function

import urllib2
import urllib
import json
import time
import os
import re

__author__          ='Wu Junkai(wujunkai20041123@outlook.com)'
__run_environment__ ='python 2.6 and above'
__edit_environment__='python 2.7.14 by IDLE'

class webpage():
    ##网页处理
    ##version 1.00.0
    def __init__(self,text):
        ##初始化
        self.text=text
    def tag(self,text):
        ##标签查找
        patt=r'(?=<%s[\w\W]{0,}>).+?(?=</%s>)'%(text,text)
        get =re.findall(patt,self.text)
        data=[]
        for i in get:
            if(re.search(r'(?<=>).+',i)):
                data.append(re.search(r'(?<=>).+',i).group())
        return data
    def __getattr__(self,text):
        ##快捷的标签查找
        data=self.tag(text)
        if(len(data)==1):
            try:
                return eval(data[0])
            except:
                return data[0]
        else:
            return data
        
    def read(self,*n):
        ##读取文件
        if(n):
            return self.text[:n[0]]
        else:
            return self.text

def net(url,**kw):
    ##网络处理
    ##version 2.00.0
    def named(text):
        ##转化特殊字符
        return re.sub(r'[\W]','_',text)
    ##数据初始化
    data=None
    headers={ 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
    ##校准 url
    if(url[-1]!='/'):
        url+='/'
    ##获取传入数据
    if('headers' in kw.keys()):
        headers=kw['headers']
    if('data' in kw.keys()):
        data=urllib.urlencode(kw['data'])
    ##解析 url
    host =re.search(r'(?<=//).+?(?=/)',url).group()
    urled=re.search(r'(?<=%s/).+(?=/)'%(host),url).group()
    ##补充 host
    if('Host' not in headers.keys()):
        headers['Host']=host
    ##是否存在 htmls 和 存在 host 所对应的目录
    if(not os.path.exists('./htmls')):
        os.mkdir('htmls')
    if(not os.path.exists('./htmls/%s'%(named(host)))):
        os.mkdir('./htmls/%s'%named(host))
    ##和 urled 所对应的文件
    if(not os.path.exists('./htmls/%s/%s.html'%(named(host),named(urled)))):
        ##若不存在此文件，则下载、补充、保存
        requ=urllib2.Request(url,data,headers)
        html=urllib2.urlopen(requ)
        text=html.read()
        print('****from url****')
        docu=open('./htmls/%s/%s.html'%(named(host),named(urled)),'w')
        docu.write(text)
        docu.close()
    else:
        ##若存在,读取
        print('****from file****')
        docu=open('./htmls/%s/%s.html'%(named(host),named(urled)),'r')
        text=docu.read()
        docu.close()
    return webpage(text)

def tree(diction,floor):
    for i in diction.keys():
        if(type(diction[i])==type({})):
            print(i+':')
            tree(diction[i],floor+1)
        else:
            for _ in xrange(floor):
                print('\t',end='')
            print(i+':'+str(diction[i]))

def debug(text):
    open('save.log','w').write(str(text))

class bilibili(object):
    def __init__(self):
        ##初始化
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
        }
    def search(self,key,**kw):
        ##vartion 1.00.0
        def urls(*kw):
            ##生成 URL
            data=kw[0]
            url='https://search.bilibili.com/'
            if('kind' in data.keys()):
                url+=data['kind']
                del data['kind']
            else:
                url+='all'
            url=url+'?'+urllib.urlencode(data)
            return url
        def analyse(text):
            ##解析搜索结果
            data=re.search(r'(?<=window.__INITIAL_STATE__=).+?}(?=;)',text).group().decode("utf-8")
            data=re.sub('null' ,'None' ,data)
            data=re.sub('false','False',data)
            data=re.sub('true' ,'True' ,data)
            data=eval(data)
            data=data['flow'][data['flow'].keys()[0]]['result']
            return data
        kw['keyword']=key
        html=urllib.unquote(net(urls(kw),headers=self.header).read()).split('\n')
        data=analyse(html[-1])
        return data
    def ranking(self,**kw):
        url='https://www.bilibili.com/ranking/'
        if('kind' in kw.keys()):
            url+=key['kind']
        debug(net(url,headers=self.header).read())
        

def main():
    m=bilibili()
    ml=m.search('青春猪头少年不会梦到',kind='all')

if(__name__=='__main__'):
    main()
