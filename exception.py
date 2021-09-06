# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: exception.py
@time: 2021/9/3 下午5:05
@desc:
"""


class GeekTimeError(BaseException):
    def __init__(self, *args,):
        super().__init__('Geek Time response is error!')
