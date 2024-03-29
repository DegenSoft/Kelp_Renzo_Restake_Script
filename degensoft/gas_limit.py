import asyncio
import random
from logging import Logger

from web3 import AsyncWeb3, AsyncHTTPProvider

from degensoft.constants import ETHEREUM_MAINNET_RPC
from degensoft.utils import force_sync


async def wait_for_gas(max_gwei: int, timeout: int = 60, logger: Logger = None,
                       stop_condition: asyncio.Event = None, ethereum_rpc: str = None) -> None:
    """
    Wait for Ethereum gas till current gas will be less than max_gwei. Use random Ethereum RPC
    :param max_gwei: max gwei
    :param timeout: wait before the next attempt
    :param logger: optional logger
    :param stop_condition: optional asyncio.Event to stop the cycle
    :param ethereum_rpc: optional ethereum rpc, otherwise will be random
    :return: None
    """
    if not ethereum_rpc:
        ethereum_rpc = random.choice(ETHEREUM_MAINNET_RPC)
    w3 = AsyncWeb3(AsyncHTTPProvider(ethereum_rpc))
    if not stop_condition:  # will be alwais True
        stop_condition = asyncio.Event()
    while not stop_condition.is_set():
        try:
            gwei = AsyncWeb3.from_wei(await w3.eth.gas_price, 'gwei')
            if gwei < max_gwei:
                if logger:
                    logger.info(f'Gas is {int(gwei)} gwei')
                break
            else:
                if logger:
                    logger.info(f'Gas {int(gwei)} gwei > {max_gwei} gwei, waiting for the cheap gas')
                for i in range(timeout):
                    await asyncio.sleep(1)
                    if stop_condition.is_set():
                        break
        except Exception as ex:
            if logger:
                logger.error(ex)


def wait_for_gas_sync(max_gwei: int, timeout: int = 60, logger: Logger = None,
                      stop_condition: asyncio.Event = None, ethereum_rpc: str = None) -> None:
    """
    Sync verion
    """
    return force_sync(wait_for_gas)(max_gwei, timeout, logger, stop_condition, ethereum_rpc)
