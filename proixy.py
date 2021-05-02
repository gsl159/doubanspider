import random
from urllib import request

from pip._vendor import requests


class Proixy():
    def __init__(self):
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
        }
        # 该接口为代理的接口
        self.url = 'https://dev.kdlapi.com/api/getproxy/?orderid=xxxxxxx&num=100&area=%E5%8C%97%E4%BA%AC%2C%E4%B8%8A%E6%B5%B7&b_pcff=1&protocol=2&method=2&an_ha=1&sp1=1&dedup=1&sep=1'

    # # 请求代理
    # def get_proixy(self):
    #     try:
    #         res = requests.get(self.url, headers=self.headers)
    #         ppp = []
    #         # 对代理返回的数据进行清洗，到达想要的效果
    #         for x in res.text.split('\n'):
    #             y = {}
    #             y['https'] = x.strip('\r')
    #             ppp.append(y)
    #         # 最后以列表包含字典的形式返回
    #         return ppp
    #     except:
    #         pass

    def getByProxy(self, url):
        # 代理ip
        proxylist = [{"http": "165.225.77.47:8800"},
                     {"http": "46.4.147.246:1080"},
                     {"http": "45.153.33.166:3128"},
                     {"http": "05.252.161.48:8080"},
                     {"http": "103.7.10.118:80"},
                     {"http": "88.198.50.103:8080"},
                     {"http": "05.252.161.48:8080"},
                     {"http": "3.225.148.200:80"},
                     {"http": "18.210.77.4:80"},
                     {"http": "39.106.223.134:80"},
                     {"http": "14.225.11.126:8080"},
                     {"http": "183.213.26.12:3128"},
                     {"http": "112.80.248.75:80"},
                     {"http": "59.56.74.51:9999"},
                     {"http": "116.117.134.134:81"},
                     {"http": "60.255.151.82:80"},
                     {"http": "220.181.111.37:80"}]
        proxy = random.choice(proxylist)
        print(proxy)
        # 在headers设置不同User-Agent，模拟不同浏览器
        agentlist = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36 Edg/89.0.774.75",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Mobile Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"]
        try:
            agent = random.choice(agentlist)
            print(agent)
            headers = {"User-Agent": agent,
                       'Cookie': 'bid=zbEWtDv0JKg; ll="118267"; __utma=30149280.1582281359.1618381927.1618381927.1618381927.1; __utmc=30149280; __utmz=30149280.1618381927.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="122147329:BY1EUrxJgns"; ck=3jlk; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.12214; __utmb=30149280.3.10.1618381927; __gads=ID=d836802aa28a4575-2280af4764c7005a:T=1618381946:S=ALNI_MZHN3sBQ5fD44rrImj5A9pG7Mwwkg'}
            # 创建处理器,用来创建opener
            proxyHandler = request.ProxyHandler(proxy)
            # 创建opener
            opener = request.build_opener(proxyHandler)
            # 创建请求对象
            req = request.Request(url, headers=headers)
            # 发送请求，返回响应
            response = opener.open(req).read().decode()
            if response == None:
                pass
            else:
                return response
        except:
            pass
