![](https://i0.hdslb.com/bfs/archive/b712fa386d1200d9c1b4d994f8f05b697dc678bc.png)
# A python module for bilibili.com  
#### Edit by Wu Junkai  
#### wujunkai20041123@outlook.com  
### introduce  
This is a module for [bilibili.com](https://www.bilibili.com).  
It was edited in python IDLE.  
### init  
you can init it like this.  
```
import my_bilibili as my
foo=my.bilibili()
```
### search  
The function is running depend on [search.bilibili.com](https://search.bilibili.com). you must give a str as keywords. Others including kind , page and so on.  
This is a table for search's  values.
 
 | variable | type | remark | 
 | --- | --- | --- |
 | keyword | str | 写了也没用 | 
 | page| int | 页数 | 
 | order| str | 下周再整理 | 
 | duration| int | `0`:`全部时长`;`1`:`10分钟以下`;`2`:`10-30分钟`;`3`:`30-60分钟`;`4`:`60分钟以上` | 
