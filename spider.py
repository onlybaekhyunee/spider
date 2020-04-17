import ssl
from urllib import request
from io import BytesIO
import gzip
import re

class Spider():
    url = 'https://www.douyu.com/g_DOTA2'
    # url = 'https://www.huya.com/g/dota2'
    root_pattern = '<div class="DyListCover-info">(.*?)</div>'
    hot_pattern = '<span class="DyListCover-hot.*?/svg>(.*?)</span>'
    user_pattern = '<h2 class="DyListCover-user.*?/svg>(.*?)</h2>'
    
    def __fetch_content(self,r):
        # 两个下划线开头，私有方法  
        # 获取请求到的html代码     
        encoding = r.info().get('Content-Encoding')
        encodetype = r.info().get('Content-Type')
        content = r.read()
        #获取html字节码，以"b’\x1f\x8b\x08"开头的 ，说明它是gzip压缩过的数据
        if encoding is None:
            # 未压缩
            if encodetype.find('utf-8') > 0: 
                # index找不到会报错，推荐find   
                page = str(content,encoding='utf-8')
                return page
            else:
                return False
        elif encoding in ('gzip','x-gzip'):
            # 获取结果为gizp，说明是被压缩的           
            buff = BytesIO(content)
            # 在内存中读写
            date = gzip.GzipFile(fileobj=buff)
            # 解压缩
            if encodetype.find('utf-8') > 0:               
                page = date.read().decode('utf-8')
                return page
            else:
                return False
        else:
            return False

    def __analysis(self,htmls):
        # html代码数据分析，利用唯一标签识别数据
        name_pops = []
        root_html = re.findall(Spider.root_pattern,htmls)
        for d in root_html:
            hot = re.findall(Spider.hot_pattern,d)
            user = re.findall(Spider.user_pattern,d)
            if hot and user:
                name_pop = {'Name':user,'PopularityValues':hot}
                name_pops.append(name_pop)
        return name_pops

    def __refine(self,anchors):
        # 数据精炼
        l = lambda anchor: {
            'Name':anchor['Name'][0].strip(),
            'PopularityValues':anchor['PopularityValues'][0].strip()
            }
        m = map(l,anchors)
        return list(m)

    def __sort(self,anchors):
        anchors = sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self,anchor):
        # 排序基准
        rn = re.findall('\d+\.?\d*',anchor['PopularityValues'])
        num = float(rn[0])
        if '万' in anchor['PopularityValues']:
            num *= 10000
        return num

    def __show(self,anchors):
        for a in anchors:
            print('%-20s'%a['Name'] + '------' + a['PopularityValues'])

    def go(self):
        # 入口方法
        context = ssl._create_unverified_context()
        # 取消证书签证
        r = request.urlopen(Spider.url,context=context)
        # 打开https网站后，会验证SSL证书，当网站使用的不是CA证书，是自签名证书时会抛出URLError异常
        htmls = self.__fetch_content(r)
        r.close()
        # 关闭连接，防止内存溢出
        if htmls:
            anchors = self.__analysis(htmls)
            anchors = self.__refine(anchors)
            anchors = self.__sort(anchors)
            self.__show(anchors)
        else:
            print('html encoding error!')
            
s = Spider()
s.go()

    