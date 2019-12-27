![](https://i0.hdslb.com/bfs/archive/1be2fd76cc98cdc6a595c05c3134fbf937a1c126.png)
# A python module just for bilibili.com
#### Edit by Wu Junkai
#### wujunkai20041123@outlook.com
### init  
This is a module for [bilibili.com](https://www.bilibili.com) . you can use it like this .  
```
import my_bilibili as my
foo=my.bilibili()
print(foo.search('刺客守则',kind='all',pages='1'))
print(foo.ranking(kind='bangumi')
```
### search  
The function 'search' is useful . you must give a str as keywords . Others including kind , page and so on .
This is a table for search's  values .
