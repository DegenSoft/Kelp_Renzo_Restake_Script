import json
import random

from web3 import AsyncWeb3
from web3.types import TxReceipt

from degensoft.utils import random_float


class BaseModule:
    CONTRACT_ADDRESS = None
    ABI = None

    def __init__(self, web3: AsyncWeb3, config):
        self.web3 = web3
        self.config = config
        if self.CONTRACT_ADDRESS:
            self.contract = self.web3.eth.contract(self.web3.to_checksum_address(self.CONTRACT_ADDRESS),
                                                   abi=json.loads(self.ABI))

    async def calculate_value(self, account):
        balance = await self.web3.eth.get_balance(account.address)
        max_value = float(self.web3.from_wei(balance, 'ether')) - self.config['max_tx_cost']

        if not self.config['amount_percent']:
            value = random_float(self.config['amount'][0],
                                 min(self.config['amount'][1], max_value))
        else:
            value = max_value * random.randint(*self.config['amount_percent']) / 100.0
        return value

    async def build_transaction(self, account, tx_call, value: int, tx_data: dict = None):
        _tx_data = {
            'value': value,
            'maxFeePerGas': int((await self.web3.eth.gas_price) * 1.5),
            'maxPriorityFeePerGas': int(await self.web3.eth.max_priority_fee * 1.5),
            'from': account.address,
            'nonce': await self.web3.eth.get_transaction_count(account.address),
        }
        if tx_data:
            _tx_data.update(tx_data)
        return await tx_call.build_transaction(_tx_data)

    async def send_and_wait_for_transaction(self, account, tx) -> TxReceipt:
        signed_tx = account.sign_transaction(tx)
        tx_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return await self.web3.eth.wait_for_transaction_receipt(tx_hash)

    async def run(self, private_key):
        raise NotImplementedError()
