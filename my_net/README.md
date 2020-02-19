# A Python Module for urllib2
　　This is a python module for urllib2 . It has so many function  that it can work as well as urllib2 and file .  
#### Edit by [wujunkai](wujunkai20041123@outlook.com "send an E-mail to me")  
### import  
　　General , using the way to import it .  
```
import my_net as net
```
### __init__  
　　General , you can init as the example . It will show the massage about how to get the web page . It will save the web page locally . There are some examples for you to use it .
###### example(with saving)
```
foo=net.net('http://www.baidu.com')
```
###### example(without save)
```
foo=net.net()
foo.url='http://www.baidu.com')
foo._visit()
```
