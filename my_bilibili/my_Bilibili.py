# !/user/bin/python
# coding=utf-8

from __future__ import print_function

import urllib
import time
import os
import re

from my_net import net

__author__          ='Wu Junkai(wujunkai20041123@outlook.com)'
__run_environment__ ='python 2.6 and above'
__edit_environment__='python 2.7.14 by IDLE'

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
  
if(__name__=='__main__'):
    m=bilibili()
    ml=m.search('青春猪头少年不会梦到',kind='all')
