# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: crawler.py
@time: 2021/9/2 上午2:27
@desc:
"""
__all__ = ['Crawler']

import asyncio
import logging

from geektime import GeekTime
from utils import mkdir, write_file

logger = logging.getLogger()


class Crawler:
    def __init__(self, phone: str, pwd: str):
        self._geek_time = GeekTime(phone, pwd)
        self.delay = 10  # Rate limit

    async def start(self) -> list:
        await self._geek_time.login()
        products_resp = await self._geek_time.fetch_products()
        products_json = await products_resp.json()
        products = products_json['data']['products']

        self.delay = len(products) * 10  # Rate limit
        return products

    async def handling_product(self, product: dict):
        if product['type'] == 'c1':
            await self._handling_c1(product)
        elif product['type'] == 'c3':
            logging.info('Do not support video download, reason is: geek use HMAC-SHA1')

    async def _handling_c1(self, product: dict):
        articles_resp = await self._geek_time.fetch_column_articles(product['id'])
        articles_json = await articles_resp.json()
        for article_info in articles_json['data']['list']:
            await asyncio.sleep(self.delay)
            article_resp = await self._geek_time.fetch_article(article_info['id'])
            article_json = await article_resp.json()

            self.generate_article_markdown(product, article_json['data'])

    @staticmethod
    def generate_article_markdown(product: dict, article: dict) -> None:
        p_id = product['id']
        a_id = article['id']
        dir_name = product['title'].strip().replace('/', '')  # Path urljoin() bug
        file_name = article['article_title'].strip().replace('/', '')  # Path urljoin() bug
        audio = article['audio_download_url']
        content = article['article_content']
        dir_path = mkdir(dir_name)
        file_path = dir_path.resolve().joinpath(file_name).with_suffix('.md')

        logger.info(f'Start generate markdown, product id={p_id}, article id={a_id}, file path: {file_path!s}')
        try:
            if audio:
                audio_content = f'<audio title="{file_name}" src="{audio}" controls="controls"></audio> \n'
                write_file(file_path, audio_content)
            write_file(file_path, content, 'a')
        except Exception as e:
            logger.error(f'Err generate markdown, product id={p_id}, article id={a_id}')
            raise e
        else:
            logger.info(f'Succeed generate markdown, product id={p_id}, article id={a_id}')

    def generate_article_video(self):
        pass

    async def end(self) -> None:
        await self._geek_time.close()
