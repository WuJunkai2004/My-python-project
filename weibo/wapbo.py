# coding=utf-8

# * a SDK for https://weibo.cn ( no copyright )
# * Wu Junkai wrote by python 2.17.7 and run with requests
# * version = 0.20.0

import requests

import json


class cookies(dict):
    '--- _cookie_ object ---'
    def __init__(self,data={}):
        for i in data:
            self[i]=data[i]

    def __str__(self):
        part = ['%s=%s'%(i,self[i]) for i in self.keys()]
        return '; '.join(part)

    def add(self,other):
        for i in other.keys():
            self[i]=other[i]


class _sub_function(object):
    'The parent class of some child functions in order to init'
    def __init__(self,_cookie_):
        self._cookie_=_cookie_
    

class _account(_sub_function):
    def login(self,username,password):
        print str(self._cookie_)
        url ="https://passport.weibo.cn/sso/login"
        head={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
            "Accept":"*/*",
            "Origin":"https://passport.weibo.cn",
            "Sec-Fetch-Site":"same-origin",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Dest":"empty",
            "Referer":"https://passport.weibo.cn/signin/login",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
            "Cookie":str(self._cookie_),
            "Content-Type":"application/x-www-form-urlencoded"
            }
        data={"username":username,
              "password":password,
              "savestate":1,
              "r":"",
              "ec":0,
              "pagerefer":"",
              "entry":"mweibo",
              "mentry":"",
              "loginfrom":"",
              "client_id":"",
              "code":"",
              "qq":"",
              "mainpageflag":1,
              "hff":"",
              "hfp":""
              }
        gets=requests.post(url,data,headers=head)
        self._cookie_.add(gets.cookies.get_dict())
        return gets.json()
        


class _emotions(_sub_function):
    pass


class _comments(_sub_function):
    pass


class _common(_sub_function):
    pass


class _oauth2(_sub_function):
    pass


class _statuses(_sub_function):
    pass


class _users(_sub_function):
    pass


class weibo(object):
    def __init__(self):
        self._cookie_=cookies()

        ##初次访问首页，获取_cookie_字段
        url ="https://weibo.cn/pub/"
        head={
            "authority":"weibo.cn",
            "scheme":"https",
            "path":"/pub/",
            "upgrade-insecure-requests":"1",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site":"none",
            "sec-fetch-mode":"navigate",
            "sec-fetch-user":"?1",
            "sec-fetch-dest":"document",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6"
            }

        self._cookie_=cookies(requests.get(url,headers=head).cookies.get_dict())

        ##prelogin，虽然不知道有什么用，不加好像也没事，但是加上一定没事
        url ="https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=MTM1MDUwMzY3MDk=&callback=jsonpcallback1595413539394"
        head={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
            "Accept":"*/*",
            "Sec-Fetch-Site":"cross-site",
            "Sec-Fetch-Mode":"no-cors",
            "Sec-Fetch-Dest":"script",
            "Referer":"https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6"
            }

        requests.get(url,headers=head)

        self.account  = _account (self._cookie_)
        self.emotions = _emotions(self._cookie_)
        self.comments = _comments(self._cookie_)
        self.common   = _common  (self._cookie_)
        self.oauth2   = _oauth2  (self._cookie_)
        self.statuses = _statuses(self._cookie_)

    def index(self):
        url ="https://weibo.cn/"
        head={
            "authority":"weibo.cn",
            "scheme":"https",
            "path":"/",
            "pragma":"no-cache",
            "upgrade-insecure-requests":"1",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site":"same-site",
            "sec-fetch-mode":"navigate",
            "sec-fetch-user":"?1",
            "sec-fetch-dest":"document",
            "referer":"https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
            "cookie":str(self._cookie_)
            }
        return requests.get(url,headers=head)
