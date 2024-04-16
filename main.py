import asyncio
import random
from sys import stderr

from loguru import logger
from itertools import cycle
from web3 import AsyncWeb3, AsyncHTTPProvider

from degensoft.config import Config
from degensoft.utils import load_lines
from degensoft.filereader import load_and_decrypt_wallets
from degensoft.gas_limit import wait_for_gas
from degensoft.logo import print_degensoft_splash
from degensoft.utils import get_explorer_tx_url
from modules import modules


def retry_on_exception(retries):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.error(f"attempt {attempt} failed with exception: {e}")
            logger.error(f"function {func.__name__} failed after {retries} attempts")

        return wrapper

    return decorator


class Worker:

    def __init__(self, config):
        self.config = config
        self.wallets = None
        self.proxies = None

    async def run(self):
        try:
            self.wallets = load_and_decrypt_wallets(self.config.wallets_file,
                                                    password=self.config.wallets_password,
                                                    shuffle=self.config.shuffle_wallets)
        except Exception as exp:
            logger.error(f'could not load wallets: {exp}')
            return
        try:
            if self.config.proxy_file:
                proxies = load_lines(self.config.proxy_file)
                if self.config.shuffle_proxies:
                    random.shuffle(proxies)
                self.proxies = cycle(proxies)
        except Exception as exp:
            logger.error(f'could not load proxies: {exp}')
        for i, private_key in enumerate(self.wallets, 1):
            is_ok = await self.process_wallet(private_key, i)
            if is_ok and i < len(self.wallets):
                delay = random.randint(*self.config.delays.wallet)
                logger.debug(f'delay for {delay} sec')
                await asyncio.sleep(delay)

    def get_prc(self, network):
        return random.choice(self.config.data['rpc'][network]) if (
                type(self.config.data['rpc'][network]) is list) else self.config.data['rpc'][network]

    @retry_on_exception(retries=3)
    async def process_wallet(self, private_key, i) -> bool:
        await wait_for_gas(self.config.max_gwei, logger=logger, ethereum_rpc=self.get_prc('ethereum'))
        web3 = AsyncWeb3(AsyncHTTPProvider(self.get_prc(self.config.network)))
        account = web3.eth.account.from_key(private_key)
        balance = await web3.eth.get_balance(account.address)
        logger.info(f'account {i}/{len(self.wallets)} {account.address} '
                    f'({web3.from_wei(balance, "ether"):.4f} ETH)')
        if not balance:
            logger.error('no balance')
            return False
        _modules = [_name for _name in self.config.data['modules'] if
                    self.config.data['modules'][_name]['enabled']]
        if self.config.shuffle_modules:
            random.shuffle(_modules)
        if self.config.random_module:
            _modules = [random.choice(_modules)]
        if 'karak' in _modules:
            _modules.remove('karak')
            _modules.append('karak')
        is_ok = False
        for i, module_name in enumerate(_modules, 1):
            res = await self.process_module(module_name, web3, account) or is_ok
            if res:
                is_ok = True
            if res and i < len(_modules):
                delay = random.randint(*self.config.delays.project)
                logger.debug(f'delay for {delay} sec')
                await asyncio.sleep(delay)
        return is_ok

    @retry_on_exception(retries=3)
    async def process_module(self, module_name, web3, account) -> bool:
        logger.debug(f'processing {module_name}...')
        cls = modules[module_name]
        module_config = self.config.data['modules'][module_name]
        if self.proxies and module_config['proxy_required']:
            proxy = next(self.proxies)
        else:
            proxy = None
        tx_receipt = await cls(web3=web3, config=module_config, proxy=proxy).run(account)
        if not tx_receipt:
            logger.error(f'FAILED')
            return False
        tx_url = get_explorer_tx_url(tx_receipt.transactionHash, self.config.data['explorer_url'][self.config.network])
        if tx_receipt.status:
            logger.info(f'OK | {tx_url}')
        else:
            logger.error(f'FAILED | {tx_url}')
        return tx_receipt.status


def setup_logger(log_file):
    logger.remove()
    logger.add(stderr,
               format="<white>{time:YYYY-MM-DD HH:mm:ss}</white> | "
                      "<level>{level: <2}</level> | "
                      "<white>{function}</white> | "
                      # "<white>{line}</white> - "
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
    try:
        main()
    except KeyboardInterrupt:
        logger.error('aborted')
