# encoding: utf-8
"""
@author: john
@contact: zhouqiang847@gmail.com
@file: session.py
@time: 2021/9/2 上午3:25
@desc:
"""
__all__ = ['Session']

from typing import Any
from types import SimpleNamespace
import asyncio
from urllib.parse import urljoin
import logging

from aiohttp import ClientSession, ClientResponse
from aiohttp.tracing import TraceConfig as TraceConfig
from aiohttp.tracing import TraceRequestStartParams, TraceRequestEndParams


logger = logging.getLogger()


async def on_request_start(
        session: ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: TraceRequestStartParams):
    msg = f'''
    Start request url {params.url}:
    request method: {params.method}
    request headers:\n {params.headers}
    '''
    logger.info(msg)


async def on_request_end(
        session: ClientSession,
        trace_config_ctx: SimpleNamespace,
        params: TraceRequestEndParams
):
    resp = params.response
    text = await resp.text()
    msg = f'''
    End request url {params.url}:
    response http code: {resp.status}
    response headers:\n {resp.headers}
    response body:\n {text}
    '''
    logger.info(msg)


class Session:
    def __init__(self, base_url: str, debug: bool = True, **kwargs: Any) -> None:
        self.base_url = base_url
        trace_configs = []
        if debug:
            trace_config = TraceConfig()
            trace_config.on_request_start.append(on_request_start)
            trace_config.on_request_end.append(on_request_end)
            trace_configs.append(trace_config)
        self._session = ClientSession(trace_configs=trace_configs, **kwargs)

    async def request(self, method: str, path: str, **kwargs: Any) -> ClientResponse:
        url = urljoin(self.base_url, path)
        async with self._session.request(
                method, url, **kwargs) as resp:
            return resp

    async def close(self) -> None:
        await asyncio.sleep(0)  # Graceful Shutdown
        await self._session.close()

    def update_headers(self, headers: dict) -> None:
        self._session.headers.update(headers)
