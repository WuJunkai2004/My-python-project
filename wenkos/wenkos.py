# coding=utf-8

# * A SDK for wenku8.net ( no copyright )
# * Wu Junkai wrote by python 3.4.4 , run in python 3,7,7

__version__='0.00.1'
__all__=[]

try:
    from urllib2   import urlopen
    from urllib2   import Request
    from urllib2   import build_opener
    from urllib2   import HTTPCookieProcessor
    from cookielib import CookieJar
except ImportError:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.request import build_opener
    from urllib.request import HTTPCookieProcessor
    from http.cookiejar import CookieJar
