import asyncio
import random

from web3 import AsyncWeb3, AsyncHTTPProvider


async def get_balance(address, rpc_url, attempts=3):
    """
    :param address: ethereum wallet address
    :param rpc_url: network rpc url
    :param attempts: numb of attempts to get balance
    :return:
    """
    for i in range(attempts):
        try:
            w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
            return await w3.eth.get_balance(address)
        except Exception as ex:
            continue


async def get_balances(address, networks: dict):
    """
    :param address: ethereum wallet address
    :param networks: {"ethereum": {"rpc": "https://rpc.url"}}
    :return: {"network_name": balance_in_wei} dict
    """
    tasks = []
    address = AsyncWeb3.to_checksum_address(address)
    for network in networks:
        rpc_url = networks[network]['rpc'] if type(networks[network]['rpc']) is str else random.choice(
            networks[network]['rpc'])
        tasks.append(get_balance(address, rpc_url))
    results = await asyncio.gather(*tasks)
    return {network: results[i] for i, network in enumerate(networks)}
