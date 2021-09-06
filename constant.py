# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: constant.py
@time: 2021/9/2 下午11:45
@desc:
"""
__all__ = ['COMMON_HEADERS', 'GEEK_BANG_URL', 'GEEK_BANG_NETLOC', 'GEEK_TIME_URL', 'GEEK_TIME_NETLOC']

from urllib.parse import urlparse

COMMON_HEADERS = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko)Chrome/81.0.4044.122 Safari/537.36'
}

GEEK_BANG_URL = 'https://account.geekbang.org'
GEEK_BANG_NETLOC = urlparse(GEEK_BANG_URL)[1]
GEEK_TIME_URL = 'https://time.geekbang.org'
GEEK_TIME_NETLOC = urlparse(GEEK_TIME_URL)[1]
