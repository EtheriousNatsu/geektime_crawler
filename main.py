# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: main.py
@time: 2021/9/2 上午3:03
@desc:
"""
import asyncio
import getpass
import logging

from crawler import Crawler

logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.INFO
)
handler = logging.FileHandler(filename='geek_crawler.log', mode='w', encoding='utf-8')
logging.root.addHandler(handler)


logger = logging.getLogger()


async def main(phone: str, password: str) -> None:
    logger.info('Start Crawling')
    geek_crawler = Crawler(phone, password)
    try:
        products = await geek_crawler.start()
        await asyncio.gather(
            *[geek_crawler.handling_product(product) for product in products]
        )
    except Exception as e:
        logger.error('Fail Crawling')
        raise e
    else:
        logger.info('Succeed Crawling')
    finally:
        await geek_crawler.end()


if __name__ == '__main__':
    cellphone = input('Please input cellphone: ')
    pwd = getpass.getpass('Please input password: ')

    asyncio.run(main(cellphone, pwd))

