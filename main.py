# encoding: utf-8

import argparse
import asyncio
import getpass
import logging
import os

from crawler import Crawler


def configure_logging():
    logging.basicConfig(
        format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        level=logging.INFO
    )
    handler = logging.FileHandler(
        filename='geek_crawler.log', mode='w', encoding='utf-8')
    logging.root.addHandler(handler)


configure_logging()
logger = logging.getLogger()


def print_menu(audio_products):
    _ = os.system('clear')
    print("------您的极客时间音频专栏列表：")
    for i, course in enumerate(audio_products):
        print(f"{i+1}. {course['title']}")


async def main(phone: str, password: str, mode: str) -> None:
    logger.info(f'start crawling with {mode} mode ...')
    geek_crawler = Crawler(phone, password)
    try:
        products = await geek_crawler.start()

        audio_products = []
        for product in products:
            if product['type'] == 'c1':
                audio_products.append({
                    'title': product['title'],
                    'id': product['id'],
                })

        if mode == 'all':
            logger.info('start crawling all audio products ...')
            await asyncio.gather(
                *[geek_crawler.handling_c1(product, len(audio_products) * 3) for product in audio_products]
            )
            return

        print_menu(audio_products)
        while True:
            choice = input("请输入要下载的课程编号(输入 q 退出): ")
            if choice == 'q':
                break
            elif choice.isnumeric() and int(choice) > 0 and int(choice) <= len(audio_products):
                index = int(choice) - 1
                await geek_crawler.handling_c1(audio_products[index])
                print_menu(audio_products)

            else:
                print("输入错误，请重新输入。")

    except Exception as e:
        logger.error('fail crawling')
        raise e
    else:
        logger.info('succeed crawling')
    finally:
        await geek_crawler.end()


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="options: all or select",
                    type=str, choices=['all', 'select'], default='select')

if __name__ == '__main__':
    args = parser.parse_args()
    cellphone = input('please input cellphone: ')
    pwd = getpass.getpass('please input password: ')

    asyncio.run(main(cellphone, pwd, args.mode))
