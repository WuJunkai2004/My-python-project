# Python object  
　　There are some python projects by myself.  
　　Some of them are no copyright.You can use it only for studing and delete it in 24 hours.  
#### Pyhon object list
|  
#### GHmusic  
　　GHmusic is a SDK by myself.It is a web crawler for https://music.ghpym.com.  
　　This is an example for use GHmusic to search "周杰伦-稻香" and download it as flac or mp3.  
```python
import GHmusic

## the password may be changed. you can follow WeChat official account and reply "音乐密码" to get the latest password.
music=GHmusic.GHmusic("52gh")

result=music.search("周杰伦-稻香")
print(result[0])

result[0].dowload.music(type="flac")
```
