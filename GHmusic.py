#coding=utf-8

# * SDK of music.ghpym.com 
# * Wu Junkai wrote by python 2.7.17
# * version = 0.80.0

import requests

from urllib import urlencode as encode
from urllib import quote as quote

#==========#
##内部调用##
#==========#
def _dict_add(*self):
    redict=[]
    for i in [i.items() for i in self]:
        redict+=i
    return dict(redict)

def _dict_str(self):
    part=['%s=%s'%(i,self[i]) for i in self.keys()]
    return '; '.join(part)

def _unicode_str(self):
    try:
        return self.encode('gbk')
    except:
        return None

#==========#
##外部接口##
#==========#
url ="https://music.ghpym.com/"
api ='https://music.ghpym.com/api/ajax.php'


header={
    "authority":"music.ghpym.com",
    "scheme":"https",
    "path":"/api/ajax.php",
    "accept":"*/*",
    "x-requested-with":"XMLHttpRequest",
    "user-agent":'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Mobile Safari/537.36',
    "origin":"https://music.ghpym.com",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
    "referer":"https://music.ghpym.com/",
    "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
    }
class GHmusic(object):
    def __init__(self,password=''):
        self.cookie=self.init()
        if(password):
            self.cookie=self.login(password)

    def init(self):
        '初始化'
        head={
            "authority":"music.ghpym.com",
            "scheme":"https",
            "path":"/",
            "cache-control":"max-age=0",
            "upgrade-insecure-requests":"1",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site":"none",
            "sec-fetch-mode":"navigate",
            "sec-fetch-user":"?1",
            "sec-fetch-dest":"document",
            "accept-encoding":"gb2312",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6"
            }

        redict =requests.get(url,headers=head).cookies.get_dict()
        return redict

    def login(self,password):
        '登录'
        head=header
        head['cookie']=_dict_str(self.cookie)
        data=encode({'action':'login','pwd':password})

        redict =requests.post(api,data,headers=head).cookies.get_dict()
        return _dict_add(self.cookie,redict)

    def search(self,key,site='qq'):
        '搜索'
        sites=['kw',#酷我
               'wy',#网易云
               'qq']#QQ
        if(site not in sites):
            return

        head=header
        head['cookie']=_dict_str(self.cookie)
        data=encode({'action':'search','site':site,'key':quote(key.decode('GBK').encode('utf-8'))})

        return [music(i,self.cookie,site)for i in requests.post(api,data,headers=head).json()[u'data']]

class _info(object):
    def __init__(self,data,cookie,site='qq'):
        if(site not in ['kw','wy','qq']):
            return

        self.pic   =_unicode_str(data[u'pic'][u'pic'])
        self.song  =_unicode_str(data[u'id'])
        self.name  =_unicode_str(data[u'name'])
        self.album =_unicode_str(data[u'album'])
        self.artist=_unicode_str(data[u'artist'])

        self.site  =site
        self.cookie=cookie
        

class music(_info):
    '歌曲'
    def __init__(self,data,cookie,site='qq'):
        _info.__init__(self,data,cookie,site)

        self.geturl  =self.url (data,cookie,site)
        self.download=self.load(data,cookie,site)

    def __dir__(self):
        return ['album', 'artist', 'download', 'geturl', 'name']

    def __str__(self):
        return '<%s - %s in %s>'%(self.artist,self.name,self.album)

    class url(_info):
        def music(self,**kw):
            if  ('type' in kw.keys()):
                if(kw['type'].lower()=='mp3'):
                    size=320
                else:
                    size=2000
            elif('size' in kw.keys()):
                size=kw['size']
            else:
                size=320

            head=header
            head['cookie']=_dict_str(self.cookie)
            data=encode({'action':'getmusicurl','site':self.site,'id':self.song,'type':size})

            print requests.post(api,data,headers=head).json()
            return {'type':'flac'if(size==2000)else'mp3','url':_unicode_str(request.post(api,data,headers=head).json()[u'url'])}

        def lyric(self):
            return '占位，不支持'

        def image(self):
            return {'type':self.pic.split('.')[-1],'url':self.pic}

        def __dir__(self):
            return ['image','lyric','music']

    class load(url):
        def music(self,**kw):
            if  ('type' in kw.keys()):
                if(kw['type'].lower()=='mp3'):
                    size=320
                else:
                    size=2000
            elif('size' in kw.keys()):
                size=kw['size']
            else:
                size=320

            head={
                "Cache-Control":"max-age=0",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6"
                }
            loadurl=music.url.music(self,size=size)

            stream =requests.get(loadurl['url'],headers=head)

            fout=open('%s - %s.%s'%(self.artist,self.name,loadurl['type']),'wb')
            fout.write(stream.content)
            fout.close()

        def lyric(self):
            head=header
            head['cookie']=_dict_str(self.cookie)
            data=encode({'action':'getmusiclrc','site':self.site,'id':self.lrc})

            songlrc=_unicode_str(requests.post(api,data,headers=head).json()[u'data'])

            fout=open('%s - %s.lrc'%(self.artist,self.name),'w+')
            fout.write(songlrc)
            fout.close()

        def image(self):
            head={
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56"
                }
            loadurl=music.url.image(self)

            stream =requests.get(loadurl['url'],headers=head)

            fout=open('%s - %s.%s'%(self.artist,self.name,loadurl['type']),'wb')
            fout.write(stream.content)
            fout.close()

        def __dir__(self):
            return ['image','lyric','music']
