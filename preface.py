""" 
2020-4-17
斗鱼爬虫前奏：
1、明确目的：直播平台主播人气
2、找到数据对应的网页
3、分析网页的结构找到数据所在的标签位置
4、模拟HTTP请求，向服务器发送这个请求，获取服务器返回给我们的HTML
5、用正则表达式提取所需数据（主播名称、人气） 
"""
""" 
2020-4-22
从豆瓣爬虫开始，舍弃urllib模块，引用Requests模块
Requests简化了urllib的诸多冗杂且无意义的操作，并提供了更强大的功能
Beautifulsoup解析网页内容
"""