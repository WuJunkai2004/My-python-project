# !/user/bin/python
# coding=utf-8

from __future__ import print_function

import urllib
import time
import os
import re

try:
    from my_net import net
except ImportError:
    raise ImportError('Sorry, can not find \'my_net\' .\nPlease view https://github.com/WuJunkai2004/Pyself/blob/master/my_net/my_net.py to download .')

__author__          ='Wu Junkai(wujunkai20041123@outlook.com)'
__version__         ='1.10.0'
__run_environment__ ='python 2.6 and above'
__edit_environment__='python 2.7.14 by IDLE'

class bilibili(object):
    def __init__(self):
        ##初始化
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
        }
    def search(self,key,**kw):
        ##搜索
        ##version 1.00.0
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
    def ranking(self,*attr):
        ##排行榜
        ##version 1.00.0
        def urls(kind):
            ##生成 url
            par={'all'     : '',
                 'origin'  : 'origin/0/0/3',
                 'bangumi' : 'bangumi/13/0/3',
                 'cinema'  : 'cinema/177/0/3',
                 'rookie'  : 'rookie/0/0/3'}
            return 'https://www.bilibili.com/ranking/'+par[kind]
        def analyse(text):
            ##解析结果
            data=[]
            for i in text:
                if(i[0]!='<'):
                    data.append(i)
            return data
        kind='all'
        if(attr):
            kind=attr[0]
        return analyse(net(urls(kind)).a)


class user(object):
    def __init__(self):
        self.name=''
        self.level=''
        self._=0
    def _login(self,**kw):
        print(net('https://passport.bilibili.com').title)

if(__name__=='__main__'):
    m=user()
    m._login()
