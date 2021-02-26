# coding=utf-8

from http import server
from http import HTTPStatus

import io
import json
import sys

__all__=['ErrorStatu', 'CookieHTTPRequestsHandler', 'EasyHTTPRequestsHandler', 'Start']

class ErrorStatu:
    '''<html><head><meta http-equiv="Content-type" content="text/html; charset=utf-8"><title>%s</title><style type="text/css">
    body {background-color: #f1f1f1;margin: 0;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}
    .container { margin: 50px auto 40px auto; width: 600px; text-align: center; }
    h1 { width: 800px; position:relative; left: -100px; letter-spacing: -1px; line-height: 60px; font-size: 60px; font-weight: 100; margin: 0px 0 50px 0; text-shadow: 0 1px 0 #fff; }
    p { color: rgba(0, 0, 0, 0.5); margin: 20px 0; line-height: 1.6; }
    </style></head><body><div class="container"><h1>%d</h1><p><strong>%s</strong></p></div></body></html>
    '''
    def __init__(self, Handler ,code):
        self.handler = Handler
        self.Response(code)

    def Error(self, name):
        error = name.split('_')
        error = ' '.join(error)
        return error.title()

    def Statu(self, code):
        for item in HTTPStatus:
            if(code==item):
                return self.Error(item.name)
        raise AttributeError(code)

    def Response(self, code):
        error = self.Statu(code)
        doc = self.__doc__%(error, code, error)
        self.handler.send_response(code)
        self.handler.send_text(doc)


class EasyHTTPRequestsHandler(server.SimpleHTTPRequestHandler):
    server_version = 'ProxyHTTP/1.0'
    def translate_path(self,path=None):
        return server.SimpleHTTPRequestHandler.translate_path(self, self.path)
        
    def translate_args(self):
        path = self.path
        try:
            args = path.split('?',1)[1]
        except IndexError:
            return {}
        words = args.split('&')
        args = {}
        for word in words:
            word = word.split('=')
            if(len(word)==1):
                word.append('')
            if(word[0] in args.keys()):
                if(type(args[word[0]])!=list):
                    args[word[0]] = [ args[word[0]] ]
                args[word[0]].append( word[1] )
            else:
                args[word[0]] = word[1]
        return args

    def translate_post(self):
        try:
            length = int(self.headers['content-length'])
        except TypeError:
            return None
        data = self.rfile.read(length)
        return data

    def send_file(self,path):
        self.end_headers()
        try:
            f = open(path, 'rb')
        except IOError:
            raise IOError('404 Not Found')
        else:
            self.copyfile(f, self.wfile)

    def send_text(self,text):
        self.end_headers()
        enc = sys.getfilesystemencoding()
        encoded = text.encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.copyfile(f, self.wfile)

    def send_headers(self,headers):
        for i in headers:
            self.send_header(i,headers[i])

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_text('Hello,world\n\t--get')

    def do_POST(self):
        print(self.headers)
        self.send_response(HTTPStatus.OK)
        self.send_text('Hello,world\n\t--post')

class PostHTTPRequestsHandler(EasyHTTPRequestsHandler):
    def parse_form(self, data):
        data = data.decode('utf-8')
        words = data.split('&')
        data = {}
        for word in words:
            word = word.split('=')
            if(len(word)==1):
                word.append('')
            if(word[0] in data.keys()):
                if(type(data[word[0]])!=list):
                    data[word[0]] = [ data[word[0]] ]
                data[word[0]].append( word[1] )
            else:
                data[word[0]] = word[1]
        return data

    def parse_json(self, data):
        data = data.decode('utf-8')
        data = json.loads(data)
        return data

    def parse_xml(self, data):
        data = data.decode('utf-8')
        try:
            import xmltodict as xml
        except ImportError:
            ErrorStatu(self,415)
            raise TypeError('415 Unsupported Media Type')
        else:
            return xml.parsers(data)

    def parse_data(self, data):
        ErrorStatu(self,415)
        raise TypeError('415 Unsupported Media Type')
        
    def translate_post(self):
        post = EasyHTTPRequestsHandler.translate_post(self)
        if('Content-Type' in self.headers):
            method = self.headers['Content-Type']
            if  (method == 'application/json'):
                return self.parse_json(data)
            elif(method == 'application/x-www-form-urlencoded'):
                return self.parse_form(data)
            elif(method == 'application/xml'):
                return self.parse_xml(data)
            elif(method == 'multipart/form-data'):
                return self.parse_data(data)
        ErrorStatu(self,415)
        raise TypeError('415 Unsupported Media Type')

    def do_POST(self):
        data = self.translate_post()
        self.send_response(HTTPStatus.OK)
        self.send_text(data)


class CookieHTTPRequestsHandler(PostHTTPRequestsHandler):
    server_version = 'CookieHTTP/1.0'
    def cookie_set(self, item, value):
        cookie = '{}={}aa=ss; Path=/'.format(item, value)
        self.send_header('Set-Cookie', cookie)

    def cookie_delete(self, item):
        cookie = '{}=; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Max-Age=0; Path=/'.format(item)
        self.send_header('Set-Cookie', cookie)

    def cookies_set(self, cookies):
        for item in cookies:
            self.cookie_set(item, cookies[item])

    def cookies_delete(self, items):
        for item in items:
            self.cookie_delete(item)


class WholeHTTPRequestsHandler(CookieHTTPRequestsHandler):
    class Interface:
        def __init__(self, handler, command):
            self.command = command
            self.handler = handler
        def __call__(self):
            ErrorStatu(self.handler, 403)

    def __getattr__(self,item):
        if(len(item)>3 and item[:3]=='do_'):
            command = item.split('_')[1]
            return self.Interface(self, command)
        raise AttributeError('Error')

'''HTTP/1.1协议中共定义了八种方法（有时也叫“动作”）来表明Request-URI指定的资源的不同操作方式：
. OPTIONS - 返回服务器针对特定资源所支持的HTTP请求方法。
                   也可以利用向Web服务器发送'*'的请求来测试服务器的功能性。
. HEAD    - 向服务器索要与GET请求相一致的响应，只不过响应体将不会被返回。
                这一方法可以在不必传输整个响应内容的情况下，就可以获取包含在响应消息头中的元信息。
. GET     - 向特定的资源发出请求。
                注意：GET方法不应当被用于产生“副作用”的操作中，例如在web app.中。
                其中一个原因是GET可能会被网络蜘蛛等随意访问。
. POST    - 向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。
                数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。
. PUT     - 向指定资源位置上传其最新内容。
. DELETE  - 请求服务器删除Request-URI所标识的资源。
. TRACE   - 回显服务器收到的请求，主要用于测试或诊断。
. CONNECT - HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。'''

def Start(handler,port=8000):
    server.test(
        HandlerClass=handler,
        ServerClass=server.ThreadingHTTPServer,
        port=port,
        bind=None,
    )


if(__name__=='__main__'):
    Start( WholeHTTPRequestsHandler )

