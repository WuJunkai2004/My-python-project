# !bin/python
# coding=utf-8

from __future__ import print_function

import urllib2
import urllib
import time
import os
import re

class net(object):
    def __init__(self,url,**kw):
        self.url=url
        ''''''
        self._create()
        try:
            self._load()
        except:
            self._visit()
            self._save()
        else:
            if(
