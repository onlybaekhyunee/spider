import requests
import json
import re
class Spider():
    def __init__(self,url):
        self.url = url

    def __fetch_content(self):
        """ 根据url请求数据 """
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
        referer = 'https://music.163.com/#/song?id=4466775'
        headers = {
            'user-agent' : user_agent,
            'referer' : self.url
            }
        params = 'LaFQT7WAgZg8eQl+zmttuXGu/H6aLxJvVL+QvmNmleQcv33aktgj7rqaBc1p1mYxyUSBayvj3rAwyEUcWfEDy8SaUjkZ83srBowSgmJ2pqtsLDm8eZUOXtfspRWU+e2Kt1mCXKJXJ/gXQS2FqAgvBpWNDd7b9UF7jo7orzcxBnqTVRLZgaMvBnwuC1HnXJ7W'
        encSecKey = '0272357f1208792170fc2807d803c76c209a3c81f1a21621a2597e1e414c71e63ad8bd3dd6a0c052053ab797dd0da2439236ba0102cfcfe188e777758da6c538f58e20ef1607096c95bc36f078d5a1760ccd161b54e4f203af2bb443e17f450e49fdd453c607d20f48752ed7b9f8731da03b4116ab5365e2b3fdf6f493ea4992'
        data = {
            'params' : params,
            'encSeckey' : encSecKey
        }
        name_id_list = re.findall('id=(\d+)',self.url)
        name_id = name_id_list[0] if len(name_id_list)>0 else ''
        target_url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_{}?csrf_token='.format(name_id)
        print(target_url)
        res = requests.post(target_url,headers=headers,data=data)
        return res

    def __get_hotcomments(self,res):
        c_json = json.loads(res.text)
        hot_comments = c_json['hotComments']
        with open('163hotcomments.txt','w',encoding='utf-8') as file:
            for each in hot_comments:
                file.write(each['user']['nickname']+':\n')
                file.write(each['content']+'\n')
                file.write('---------------------------------\n')
    
    def go(self):
        """ 入口文件 """
        res = self.__fetch_content()
        if res.status_code == 200:
            # 从服务器获取的数据不为空
            with open('163.txt','w',encoding='utf-8') as file:
                file.write(res.text)
            # 解析json数据
            self.__get_hotcomments(res)
       

url = 'https://music.163.com/#/song?id=4466775'
s = Spider(url)
s.go()
