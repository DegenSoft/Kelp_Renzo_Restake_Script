import asyncio
import random
import requests

from loguru import logger
from eth_account.messages import encode_defunct
from degensoft.utils import random_float
from modules.base import BaseModule
from modules.erc20 import Erc20Token


class Karak(BaseModule):
    CONTRACT_ADDRESS = '0x399f22ae52a18382a67542b3De9BeD52b7B9A4ad'
    RENZO_EZETH_CONTRACT_ADDRESS = '0x2416092f143378750bb29b79eD961ab195CcEea5'
    KARAK_EZETH_CONTRACT_ADDRESS = '0xC190924A68B570F943a2974d46F0D8c5E742BBcB'
    KARAK_REF_LIST = ('6vnaa', 'MWJHt', 'kX5PY', 'nsIXh', 'jPIVZ')
    ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"CrossedDepositLimit","type":"error"},{"inputs":[],"name":"ECDSAInvalidSignature","type":"error"},{"inputs":[{"internalType":"uint256","name":"length","type":"uint256"}],"name":"ECDSAInvalidSignatureLength","type":"error"},{"inputs":[{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"ECDSAInvalidSignatureS","type":"error"},{"inputs":[],"name":"EnforcedPause","type":"error"},{"inputs":[],"name":"ExpectedPause","type":"error"},{"inputs":[],"name":"ExpiredSign","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidSignature","type":"error"},{"inputs":[],"name":"InvalidVaultAdminFunction","type":"error"},{"inputs":[],"name":"MaxStakerVault","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NoHandoverRequest","type":"error"},{"inputs":[],"name":"NotDelegationSupervisor","type":"error"},{"inputs":[],"name":"NotEnoughShares","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"PermitFailed","type":"error"},{"inputs":[],"name":"Reentrancy","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"inputs":[],"name":"UnauthorizedCallContext","type":"error"},{"inputs":[],"name":"UpgradeFailed","type":"error"},{"inputs":[],"name":"VaultNotAChildVault","type":"error"},{"inputs":[],"name":"VaultNotFound","type":"error"},{"inputs":[],"name":"ZeroAddress","type":"error"},{"inputs":[],"name":"ZeroShares","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"}],"name":"NewVault","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"roles","type":"uint256"}],"name":"RolesUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"UpgradedAllVaults","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"},{"indexed":true,"internalType":"address","name":"vault","type":"address"}],"name":"UpgradedVault","type":"event"},{"inputs":[],"name":"SIGNED_DEPOSIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"cancelOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newVaultImpl","type":"address"}],"name":"changeImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"vault","type":"address"},{"internalType":"address","name":"newVaultImpl","type":"address"}],"name":"changeImplementationForVault","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"completeOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"delegationSupervisor","outputs":[{"internalType":"contract IDelegationSupervisor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"depositToken","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"enum IVault.AssetType","name":"assetType","type":"uint8"}],"name":"deployVault","outputs":[{"internalType":"contract IVault","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"deposit","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"components":[{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IVaultSupervisor.Signature","name":"permit","type":"tuple"},{"components":[{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IVaultSupervisor.Signature","name":"vaultAllowance","type":"tuple"}],"name":"depositWithSignature","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"getDeposits","outputs":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"assets","type":"uint256[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVaults","outputs":[{"internalType":"contract IVault[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"grantRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"hasAllRoles","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"hasAnyRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vault","type":"address"}],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegationSupervisor","type":"address"},{"internalType":"address","name":"_vaultImpl","type":"address"},{"internalType":"contract ILimiter","name":"_limiter","type":"address"},{"internalType":"address","name":"_manager","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"result","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"ownershipHandoverExpiresAt","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"toPause","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"redeemShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"removeShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"renounceRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"requestOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"revokeRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"rolesOf","outputs":[{"internalType":"uint256","name":"roles","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"bytes","name":"fn","type":"bytes"}],"name":"runAdminOperation","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILimiter","name":"limiter","type":"address"}],"name":"setLimiter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"}]'

    async def run(self, account):
        await self._login_karak(account)

        ezeth = Erc20Token(self.web3, self.RENZO_EZETH_CONTRACT_ADDRESS)
        balance = await ezeth.balance_of(account.address)
        logger.debug(f'ezETH balance {self.web3.from_wei(balance, "ether")} ezETH')
        if not balance:
            logger.error('no ezETH balance')
            return

        value = self._get_value(balance)
        allowance = await ezeth.allowance(account.address, self.KARAK_EZETH_CONTRACT_ADDRESS)
        if allowance < value:
            tx_receipt = await ezeth.approve(account, self.KARAK_EZETH_CONTRACT_ADDRESS, value)
            if tx_receipt.status:
                logger.debug('approve is ok')
                logger.debug('wait for 3 sec...')
                await asyncio.sleep(3)
            else:
                raise RuntimeError('failed to approve')

        tx_call = self.contract.functions.deposit(self.KARAK_EZETH_CONTRACT_ADDRESS, value)
        logger.debug(f'{self.web3.from_wei(value, "ether"):.4f} ezETH -> Karak')
        tx = await self.build_transaction(account, tx_call, 0)
        return await self.send_and_wait_for_transaction(account, tx)

    def _get_value(self, balance):
        _max_value = float(self.web3.from_wei(balance, 'ether'))
        if not self.config['amount_percent']:
            value = random_float(self.config['amount'][0],
                                 min(self.config['amount'][1], _max_value))
        else:
            value = _max_value * random.randint(*self.config['amount_percent']) / 100.0
        return self.web3.to_wei(value, 'ether')

    def _get_headers(self):
        return {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6,uk;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://app.karak.network',
            'Referer': 'https://app.karak.network/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    async def _login_karak(self, account):
        headers = self._get_headers()
        ref = random.choice(self.KARAK_REF_LIST)
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None

        # checking wallet already registered
        params = {
            'batch': '1',
            'input': '{"0":{"wallet":"%s"}}' % account.address,
        }
        response = requests.get('https://restaking-backend.karak.network/getReferrals', params=params,
                                headers=headers, proxies=proxies)
        if response.status_code == 200:
            logger.debug('already registered in karak')
            return

        logger.debug('registering wallet in karak...')

        # checking referal code
        params = {
            'batch': '1',
            'input': '{"0":{"referralCode":"%s"}}' % ref,
        }
        response = requests.get('https://restaking-backend.karak.network/verifyReferral', params=params,
                                headers=headers, proxies=proxies)
        if response.status_code != 200:
            raise RuntimeError('bad referal code: %s' % ref)

        # getting message to sign
        params = {'batch': '1'}
        json_data = {'0': {'referralCode': '6n3sK'}}

        response = requests.post('https://restaking-backend.karak.network/startRegisterWallet', params=params,
                                 headers=headers, json=json_data, proxies=proxies)
        if response.status_code != 200:
            raise RuntimeError('could not get message to sign in to karak: %s' % response.text)
        res = response.json()
        message = res[0]['result']['data']['message']

        # signing message
        signature = account.sign_message(encode_defunct(text=message))

        # registering
        json_data = {
            '0': {
                'wallet': account.address,
                'walletDraftId': res[0]['result']['data']['walletDraftId'],
                'signature': signature.signature.hex(),
            },
        }
        logger.debug('wait for 3 sec...')
        await asyncio.sleep(3)
        response = requests.post('https://restaking-backend.karak.network/finishRegisterWallet', params=params,
                                 headers=headers, json=json_data, proxies=proxies)
        if response.status_code != 200:
            raise RuntimeError('error registering wallet: %s' % response.json()[0]['error']['message'])

        logger.debug('wallet registered!')
