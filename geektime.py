# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: geektime.py
@time: 2021/9/2 上午2:48
@desc:
"""
__all__ = ['GeekTime']

import re
from typing import Any
from copy import deepcopy
import logging

from aiohttp import ClientResponse

from session import Session
from exception import GeekTimeError
from constant import *

logger = logging.getLogger()


class GeekBangSession(Session):

    def __init__(self, **kwargs: Any) -> None:
        self.headers = headers = deepcopy(COMMON_HEADERS)
        headers['Host'] = GEEK_BANG_NETLOC
        headers['Origin'] = GEEK_BANG_URL
        super().__init__(GEEK_BANG_URL, headers=self.headers, **kwargs)


class GeekTimeSession(Session):

    def __init__(self, **kwargs: Any) -> None:
        self.headers = headers = deepcopy(COMMON_HEADERS)
        headers['Host'] = GEEK_TIME_NETLOC
        headers['Origin'] = GEEK_TIME_URL
        super().__init__(GEEK_TIME_URL, headers=self.headers, **kwargs)


class GeekTimeCookie:
    def __init__(self):
        self._cookies = {}

    @property
    def cookie_string(self) -> str:
        return ';'.join([f'{k}={v}' for k, v in self._cookies.items()])

    def load_cookies(self, cookies: list) -> None:
        cookies_list = []
        for cookie in cookies:
            cookies_list.append(re.sub(".xpires=.*?;", "", cookie).split(';')[0])
        res = self.list_to_dict(cookies_list)
        self._cookies = {**self._cookies, **res}

    @staticmethod
    def list_to_dict(l: list) -> dict:
        result = {}
        for ind in l:
            try:
                ind = ind.split('=')
                result[ind[0]] = ind[1]
            except IndexError:
                continue
        return result


class GeekTime:
    def __init__(self, phone: str, password: str):
        """
        :param phone: phone number
        :param password: password
        """
        self.phone = phone
        self.password = password
        self._geek_bang_client = GeekBangSession()
        self._geek_time_client = GeekTimeSession()
        self._geek_time_cookie = GeekTimeCookie()

    async def login(self) -> None:
        """login"""
        logger.info('Start login')

        path = 'account/ticket/login'
        data = {
            'country': 86,
            'cellphone': self.phone,
            'password': self.password,
            'captcha': '',
            'remember': 1,
            'platform': 3,
            'appid': 1,
            'source': ''
        }

        resp = await self._geek_bang_client.request(
            'post',
            path,
            json=data
        )

        await self._raise_for_status(resp)

        self._geek_time_cookie.load_cookies(resp.headers.getall('Set-Cookie'))
        self._geek_time_client.update_headers(
            {'Cookie': self._geek_time_cookie.cookie_string}
        )

        logger.info('Succeed login')

    async def fetch_products(self) -> ClientResponse:
        """products list"""
        logger.info('Start fetch products')

        path = 'serv/v3/learn/product'
        data = {
            'desc': True,
            'expire': 1,
            'last_learn': 0,
            'learn_status': 0,
            'prev': 0,
            'size': 20,
            'sort': 1,
            'type': '',
            'with_learn_count': 1
        }

        resp = await self._geek_time_client.request('post', path, json=data)
        await self._raise_for_status(resp)

        logger.info('Succeed fetch products')

        return resp

    async def fetch_column_articles(self, cid: str) -> ClientResponse:
        """Fetch articles

        :param cid: product id
        """
        logger.info(f'Start fetch articles, product id is {cid}')

        path = 'serv/v1/column/articles'
        data = {
            'cid': cid,
            'order': 'earliest',
            'prev': 0,
            'size': 500,
            'sample': False
        }

        resp = await self._geek_time_client.request('post', path, json=data)
        await self._raise_for_status(resp)

        logger.info(f'Succeed fetch articles, product id is {cid}')

        return resp

    async def fetch_article(self, article_id: str) -> ClientResponse:
        """Fetch article"""
        logger.info(f'Start fetch article, article id is {article_id}')

        path = 'serv/v1/article'
        data = {
            'id': article_id,
            'include_neighbors': True,
            'is_freelyread': True
        }

        resp = await self._geek_time_client.request('post', path, json=data)
        await self._raise_for_status(resp)

        logger.info(f'Succeed fetch article, article id is {article_id}')

        return resp

    async def close(self):
        await self._geek_bang_client.close()
        await self._geek_time_client.close()

    @staticmethod
    async def _raise_for_status(resp: ClientResponse) -> None:
        data = await resp.json()
        if not resp.ok or data.get('code', -1) == -1:
            raise GeekTimeError()
        elif resp.ok and resp.status == 451:
            logger.error('Geek time rate limit, please slow you program')
            exit(-1)
