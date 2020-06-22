from pip._vendor import requests


class Proixy():
    def __init__(self):
        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
        }
        # 该接口为代理的接口
        self.url = 'https://dev.kdlapi.com/api/getproxy/?orderid=xxxxxxx&num=100&area=%E5%8C%97%E4%BA%AC%2C%E4%B8%8A%E6%B5%B7&b_pcff=1&protocol=2&method=2&an_ha=1&sp1=1&dedup=1&sep=1'

    # 请求代理
    def get_proixy(self):
        try:
            res = requests.get(self.url, headers=self.headers)
            ppp = []
            # 对代理返回的数据进行清洗，到达想要的效果
            for x in res.text.split('\n'):
                y = {}
                y['https'] = x.strip('\r')
                ppp.append(y)
            # 最后以列表包含字典的形式返回
            return ppp
        except:
            pass
