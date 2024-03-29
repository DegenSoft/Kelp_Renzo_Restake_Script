import asyncio
import json
import random
import time
from sys import stderr

import aiohttp
from loguru import logger
from web3 import AsyncWeb3, AsyncHTTPProvider

from degensoft.config import Config
from degensoft.filereader import load_and_decrypt_wallets
from degensoft.gas_limit import wait_for_gas
from degensoft.logo import print_degensoft_splash
from degensoft.utils import get_explorer_tx_url


class Worker:

    def __init__(self, config):
        self.config = config

    async def run(self):
        ...


def setup_logger(log_file):
    logger.remove()
    logger.add(stderr,
               format="<white>{time:YYYY-MM-DD HH:mm:ss}</white> | "
                      "<level>{level: <2}</level> | "
                      "<white>{function}</white> | "
                      "<white>{line}</white> - "
                      "<white>{message}</white>")
    logger.add(log_file)


def main():
    config = Config()
    try:
        config.load('config.local.json')
    except FileNotFoundError:
        config.load('config.json')

    if config.show_degensoft_logo:
        print_degensoft_splash()

    setup_logger(config.log_file)
    logger.info('STARTING')

    w = Worker(config=config)
    asyncio.run(w.run())

    logger.info('FINISHING')


if __name__ == '__main__':
    main()
