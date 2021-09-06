# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: utils.py
@time: 2021/9/4 下午1:37
@desc:
"""
__all__ = ['mkdir', 'touch_file', 'write_file']

from typing import Union
from pathlib import Path


def mkdir(path: Union[str, Path]) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

    return p


def touch_file(path: Union[str, Path]) -> Path:
    p = Path(path)
    p.touch(exist_ok=True)

    return path


def write_file(path: Union[str, Path], content: str, mode: str = 'w') -> Path:
    p = Path(path).resolve()
    with p.open(mode, encoding='utf-8') as f:
        f.write(content)

    return p


