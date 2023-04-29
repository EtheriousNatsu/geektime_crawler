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
from pathlib import Path

import aiohttp

from geektime import GeekTime
from utils import mkdir, write_file

logger = logging.getLogger()


class Crawler:
    def __init__(self, phone: str, pwd: str):
        self._geek_time = GeekTime(phone, pwd)

    async def start(self) -> list:
        await self._geek_time.login()
        products_resp = await self._geek_time.fetch_products()
        products_json = await products_resp.json()
        products = products_json['data']['products']

        # self.delay = len(products) * 10  # Rate limit
        return products

    async def handling_product(self, product: dict):
        if product['type'] == 'c1':
            await self.handling_c1(product)
        elif product['type'] == 'c3':
            logging.info(
                'Do not support video download, reason is: geek use HMAC-SHA1')

    async def handling_c1(self, product: dict, delay: int = 3):
        articles_resp = await self._geek_time.fetch_column_articles(product['id'])
        articles_json = await articles_resp.json()

        title = product['title'].strip().replace('/', '')
        title_path = mkdir(title)
        audio_path = mkdir(f"{title}/audios")
        for article_info in articles_json['data']['list']:
            await asyncio.sleep(delay) # Rate limit
            article_resp = await self._geek_time.fetch_article(article_info['id'])
            article_json = await article_resp.json()

            await self.generate_article_markdown(title, title_path, audio_path, article_json['data'])

    @staticmethod
    async def generate_article_markdown(title: str, title_path: Path, audio_path: Path, article: dict) -> None:
        file_name = article['article_title'].strip().replace('/', '')
        audio = article['audio_download_url']
        content = article['article_content']
        file_path = title_path.resolve().joinpath(file_name).with_suffix('.md')

        logger.info(
            f'start generate markdown, {title}, article={file_name}, file path: {file_path!s}')
        try:
            if audio:
                mp3_name = audio[audio.rfind("/")+1:]
                audio_file_name = audio_path.resolve().joinpath(f'{mp3_name}')
                await Crawler.download_audio(audio, audio_file_name)
                audio_content = f'# {file_name}\r\n<audio title="{file_name}" src="./audios/{mp3_name}" controls="controls"></audio> \n'
                write_file(file_path, audio_content)
            write_file(file_path, content, 'a')
        except Exception as e:
            logger.error(
                f'err {title}, article={file_name}')
            raise e
        else:
            logger.info(
                f'succeed {title}, article={file_name}')

    def generate_article_video(self):
        pass

    @staticmethod
    async def download_audio(mp3_url: str, audio_path: Path):
        async with aiohttp.ClientSession() as session:
            async with session.get(mp3_url) as response:
                with audio_path.resolve().open('wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

    async def end(self) -> None:
        await self._geek_time.close()
