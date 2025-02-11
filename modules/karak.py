import os
import asyncio
import random
import json

import requests
import ua_generator
from eth_account.messages import encode_defunct
from loguru import logger

from degensoft.utils import random_float
from modules.base import BaseModule
from modules.erc20 import Erc20Token


class Karak(BaseModule):
    CONTRACTS = {
        42161: '0x399f22ae52a18382a67542b3De9BeD52b7B9A4ad',  # Arbitrum
        1: '0x54e44DbB92dBA848ACe27F44c0CB4268981eF1CC',  # Ethereum    
    }

    DELEGATION_SUPERVISER_CONTRACTS = {
        42161: '0x48769803c0449532Bd23DB3A413152632753c8f0',  # Arbitrum
        1: '0xAfa904152E04aBFf56701223118Be2832A4449E0' # Ethereum
    }
    # CONTRACT_ADDRESS = '0x399f22ae52a18382a67542b3De9BeD52b7B9A4ad'
    RENZO_EZETH_CONTRACT_ADDRESS = '0x2416092f143378750bb29b79eD961ab195CcEea5'
    KARAK_EZETH_CONTRACT_ADDRESS = '0xC190924A68B570F943a2974d46F0D8c5E742BBcB'
    PUFFER_PUFFETH_CONTRACT_ADDRESS = '0xD9A442856C234a39a81a089C06451EBAa4306a72'
    KARAK_PUFFETH_CONTRACT_ADDRESS = '0x68754d29f2e97B837Cb622ccfF325adAC27E9977'
    KARAK_REF_LIST = ['6vnaa', 'MWJHt', 'kX5PY', 'nsIXh', 'jPIVZ']
   
    DELEGATION_SUPERVISER_ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"ArrayLengthsNotEqual","type":"error"},{"inputs":[],"name":"EnforcedPause","type":"error"},{"inputs":[],"name":"ExpectedPause","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidInput","type":"error"},{"inputs":[],"name":"InvalidWithdrawalDelay","type":"error"},{"inputs":[],"name":"MinWithdrawDelayNotPassed","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NoElementsInArray","type":"error"},{"inputs":[],"name":"NoHandoverRequest","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"NotStaker","type":"error"},{"inputs":[],"name":"Reentrancy","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"inputs":[],"name":"UnauthorizedCallContext","type":"error"},{"inputs":[],"name":"UpgradeFailed","type":"error"},{"inputs":[],"name":"WithdrawAlreadyCompleted","type":"error"},{"inputs":[],"name":"WithdrawerNotCaller","type":"error"},{"inputs":[],"name":"ZeroShares","type":"error"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":true,"internalType":"address","name":"staker","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"address","name":"withdrawer","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"withdrawRoot","type":"bytes32"}],"name":"FinishedWithdrawal","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"roles","type":"uint256"}],"name":"RolesUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":true,"internalType":"address","name":"staker","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"address","name":"withdrawer","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"}],"name":"StartedWithdrawal","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"cancelOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"completeOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"fetchQueuedWithdrawals","outputs":[{"components":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"address","name":"delegatedTo","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"start","type":"uint256"},{"components":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"withdrawer","type":"address"}],"internalType":"struct Withdraw.WithdrawRequest","name":"request","type":"tuple"}],"internalType":"struct Withdraw.QueuedWithdrawal[]","name":"queuedWithdrawals","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"address","name":"delegatedTo","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"start","type":"uint256"},{"components":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"withdrawer","type":"address"}],"internalType":"struct Withdraw.WithdrawRequest","name":"request","type":"tuple"}],"internalType":"struct Withdraw.QueuedWithdrawal[]","name":"startedWithdrawals","type":"tuple[]"}],"name":"finishWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"grantRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"hasAllRoles","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"hasAnyRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vaultSupervisor","type":"address"},{"internalType":"uint256","name":"minWithdrawDelay","type":"uint256"},{"internalType":"address","name":"manager","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"address","name":"delegatedTo","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"start","type":"uint256"},{"components":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"withdrawer","type":"address"}],"internalType":"struct Withdraw.WithdrawRequest","name":"request","type":"tuple"}],"internalType":"struct Withdraw.QueuedWithdrawal","name":"withdrawal","type":"tuple"}],"name":"isWithdrawPending","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"result","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"ownershipHandoverExpiresAt","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"toPause","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"renounceRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"requestOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"revokeRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"rolesOf","outputs":[{"internalType":"uint256","name":"roles","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"withdrawer","type":"address"}],"internalType":"struct Withdraw.WithdrawRequest[]","name":"withdrawalRequests","type":"tuple[]"}],"name":"startWithdraw","outputs":[{"internalType":"bytes32[]","name":"withdrawalRoots","type":"bytes32[]"},{"components":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"address","name":"delegatedTo","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"start","type":"uint256"},{"components":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"},{"internalType":"address","name":"withdrawer","type":"address"}],"internalType":"struct Withdraw.WithdrawRequest","name":"request","type":"tuple"}],"internalType":"struct Withdraw.QueuedWithdrawal[]","name":"withdrawConfigs","type":"tuple[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"delay","type":"uint256"}],"name":"updateMinWithdrawDelay","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"withdrawalDelay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

    ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"CrossedDepositLimit","type":"error"},{"inputs":[],"name":"ECDSAInvalidSignature","type":"error"},{"inputs":[{"internalType":"uint256","name":"length","type":"uint256"}],"name":"ECDSAInvalidSignatureLength","type":"error"},{"inputs":[{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"ECDSAInvalidSignatureS","type":"error"},{"inputs":[],"name":"EnforcedPause","type":"error"},{"inputs":[],"name":"ExpectedPause","type":"error"},{"inputs":[],"name":"ExpiredSign","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"InvalidSignature","type":"error"},{"inputs":[],"name":"InvalidSwapper","type":"error"},{"inputs":[],"name":"InvalidSwapperRouteLength","type":"error"},{"inputs":[],"name":"InvalidVaultAdminFunction","type":"error"},{"inputs":[],"name":"MaxStakerVault","type":"error"},{"inputs":[],"name":"MigrationRedeemFailed","type":"error"},{"inputs":[],"name":"MigrationSwapFailed","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NoHandoverRequest","type":"error"},{"inputs":[],"name":"NotDelegationSupervisor","type":"error"},{"inputs":[],"name":"NotEnoughShares","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"PermitFailed","type":"error"},{"inputs":[],"name":"Reentrancy","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"inputs":[],"name":"UnauthorizedCallContext","type":"error"},{"inputs":[],"name":"UpgradeFailed","type":"error"},{"inputs":[],"name":"VaultNotAChildVault","type":"error"},{"inputs":[],"name":"VaultNotFound","type":"error"},{"inputs":[],"name":"ZeroAddress","type":"error"},{"inputs":[],"name":"ZeroShares","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":true,"internalType":"address","name":"staker","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"address","name":"withdrawer","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"withdrawRoot","type":"bytes32"}],"name":"FinishedWithdrawal","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"staker","type":"address"},{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":false,"internalType":"address","name":"shareToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"}],"name":"GaveShares","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"}],"name":"NewVault","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"pendingOwner","type":"address"}],"name":"OwnershipHandoverRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"staker","type":"address"},{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":false,"internalType":"address","name":"shareToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"}],"name":"ReturnedShares","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"roles","type":"uint256"}],"name":"RolesUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":true,"internalType":"address","name":"staker","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"address","name":"withdrawer","type":"address"},{"indexed":false,"internalType":"uint256","name":"shares","type":"uint256"}],"name":"StartedWithdrawal","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"UpgradedAllVaults","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"},{"indexed":true,"internalType":"address","name":"vault","type":"address"}],"name":"UpgradedVault","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"},{"indexed":true,"internalType":"address","name":"oldAsset","type":"address"},{"indexed":true,"internalType":"address","name":"newAsset","type":"address"},{"indexed":false,"internalType":"uint256","name":"oldAssetIn","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newAssetOut","type":"uint256"},{"indexed":false,"internalType":"string","name":"newName","type":"string"},{"indexed":false,"internalType":"string","name":"newSymbol","type":"string"},{"indexed":false,"internalType":"enum IVault.AssetType","name":"newAssetType","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"newAssetLimit","type":"uint256"}],"name":"VaultSwap","type":"event"},{"inputs":[],"name":"SIGNED_DEPOSIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"cancelOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newVaultImpl","type":"address"}],"name":"changeImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"vault","type":"address"},{"internalType":"address","name":"newVaultImpl","type":"address"}],"name":"changeImplementationForVault","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"completeOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"delegationSupervisor","outputs":[{"internalType":"contract IDelegationSupervisor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"depositToken","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"enum IVault.AssetType","name":"assetType","type":"uint8"}],"name":"deployVault","outputs":[{"internalType":"contract IVault","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"minSharesOut","type":"uint256"}],"name":"deposit","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"minSharesOut","type":"uint256"}],"name":"depositAndGimmie","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"minSharesOut","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"components":[{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IVaultSupervisor.Signature","name":"permit","type":"tuple"},{"components":[{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct IVaultSupervisor.Signature","name":"vaultAllowance","type":"tuple"}],"name":"depositWithSignature","outputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"getDeposits","outputs":[{"internalType":"contract IVault[]","name":"vaults","type":"address[]"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"assets","type":"uint256[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getVaults","outputs":[{"internalType":"contract IVault[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"gimmieShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"grantRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"hasAllRoles","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"hasAnyRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"vault","type":"address"}],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_delegationSupervisor","type":"address"},{"internalType":"address","name":"_vaultImpl","type":"address"},{"internalType":"contract ILimiter","name":"_limiter","type":"address"},{"internalType":"address","name":"_manager","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"oldVault","type":"address"},{"internalType":"contract IVault","name":"newVault","type":"address"},{"internalType":"uint256","name":"oldShares","type":"uint256"},{"internalType":"uint256","name":"minNewShares","type":"uint256"},{"internalType":"bytes","name":"swapperOtherParams","type":"bytes"}],"name":"migrate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"result","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"pendingOwner","type":"address"}],"name":"ownershipHandoverExpiresAt","outputs":[{"internalType":"uint256","name":"result","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"toPause","type":"bool"}],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"redeemShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20[]","name":"inputAsset","type":"address[]"},{"internalType":"contract IERC20[]","name":"outputAsset","type":"address[]"},{"internalType":"contract ISwapper","name":"swapper","type":"address"}],"name":"registerSwapperForRoutes","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"},{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"removeShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"renounceRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"requestOwnershipHandover","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"returnShares","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"roles","type":"uint256"}],"name":"revokeRoles","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"rolesOf","outputs":[{"internalType":"uint256","name":"roles","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"internalType":"bytes","name":"fn","type":"bytes"}],"name":"runAdminOperation","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILimiter","name":"limiter","type":"address"}],"name":"setLimiter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IVault","name":"vault","type":"address"},{"components":[{"internalType":"contract IERC20","name":"newDepositToken","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"enum IVault.AssetType","name":"assetType","type":"uint8"},{"internalType":"uint256","name":"assetLimit","type":"uint256"}],"internalType":"struct IVault.SwapAssetParams","name":"params","type":"tuple"},{"internalType":"uint256","name":"minNewAssetAmount","type":"uint256"},{"internalType":"bytes","name":"swapperParams","type":"bytes"}],"name":"vaultSwap","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

    async def run(self, account):
        if self.config.get('withdraw_start'):
             chain_id = await self.web3.eth.chain_id
             self.contract = self.web3.eth.contract(self.web3.to_checksum_address(self.DELEGATION_SUPERVISER_CONTRACTS[chain_id]),
                                                abi=json.loads(self.DELEGATION_SUPERVISER_ABI))
             self.dep_contract = self.web3.eth.contract(self.web3.to_checksum_address(self.CONTRACTS[chain_id]),
                                                abi=json.loads(self.ABI))
             erc20_contract_address = self.KARAK_PUFFETH_CONTRACT_ADDRESS if chain_id == 1 \
                else self.KARAK_EZETH_CONTRACT_ADDRESS
             token = Erc20Token(self.web3, erc20_contract_address)
             symbol = await token.symbol()
             balance_pool = await self.dep_contract.functions.getDeposits(account.address).call()
             logger.debug(f'{symbol} balance {self.web3.from_wei(balance_pool[3][0], "ether")} {symbol} in Karak pool')
             if not balance_pool:
                logger.error(f'no {symbol} balance')
                return (f'no {symbol} balance')
             value = self._get_value(balance_pool[3][0])
             karak_contract_address = self.KARAK_PUFFETH_CONTRACT_ADDRESS if chain_id == 1 \
                else self.KARAK_EZETH_CONTRACT_ADDRESS
             tx_call = self.contract.functions.startWithdraw([([karak_contract_address], [value], account.address)])
             logger.debug(f'Karak -> {self.web3.from_wei(value, "ether"):.4f} {symbol} | In queue, come back in 7 days')
             tx = await self.build_transaction(account, tx_call, 0)
             return await self.send_and_wait_for_transaction(account, tx)
        elif self.config.get('withdraw_finish'):
             chain_id = await self.web3.eth.chain_id
             self.contract = self.web3.eth.contract(self.web3.to_checksum_address(self.DELEGATION_SUPERVISER_CONTRACTS[chain_id]),
                                                abi=json.loads(self.DELEGATION_SUPERVISER_ABI))
             self.dep_contract = self.web3.eth.contract(self.web3.to_checksum_address(self.CONTRACTS[chain_id]),
                                                abi=json.loads(self.ABI))
             erc20_contract_address = self.KARAK_PUFFETH_CONTRACT_ADDRESS if chain_id == 1 \
                else self.KARAK_EZETH_CONTRACT_ADDRESS
             token = Erc20Token(self.web3, erc20_contract_address)
             symbol = await token.symbol()
             balance_pool = await self.contract.functions.fetchQueuedWithdrawals(account.address).call()
             print(balance_pool)
             logger.debug(f'{symbol} balance for withdraw {self.web3.from_wei(balance_pool[0][4][1][0], "ether")} {symbol} in Karak pool')
             if not balance_pool:
                logger.error(f'No {symbol} balance queued for withdraw')
                return (f'No {symbol} balance queued for withdraw')
             tx_call = self.contract.functions.finishWithdraw(balance_pool)
             logger.debug(f'Karak -> {self.web3.from_wei(balance_pool[0][4][1][0], "ether"):.4f} {symbol} ')
             tx = await self.build_transaction(account, tx_call, 0)
             return await self.send_and_wait_for_transaction(account, tx)
        else:    
            await self._login_karak(account)
            if self.config.get('registration_only'):
                return True

            chain_id = await self.web3.eth.chain_id

            self.contract = self.web3.eth.contract(self.web3.to_checksum_address(self.CONTRACTS[chain_id]),
                                                abi=json.loads(self.ABI))
            erc20_contract_address = self.PUFFER_PUFFETH_CONTRACT_ADDRESS if chain_id == 1 \
                else self.RENZO_EZETH_CONTRACT_ADDRESS
            token = Erc20Token(self.web3, erc20_contract_address)
            symbol = await token.symbol()
            balance = await token.balance_of(account.address)
            logger.debug(f'{symbol} balance {self.web3.from_wei(balance, "ether")} {symbol}')
            if not balance:
                logger.error(f'no {symbol} balance')

            value = self._get_value(balance)
            karak_contract_address = self.KARAK_PUFFETH_CONTRACT_ADDRESS if chain_id == 1 \
                else self.KARAK_EZETH_CONTRACT_ADDRESS
            allowance = await token.allowance(account.address, karak_contract_address)
            if allowance < value:
                logger.debug('approving...')
                tx_receipt = await token.approve(account, karak_contract_address, value)
                if tx_receipt.status:
                    logger.debug('approve is ok!')
                    delay = random.randint(15, 25)
                    logger.debug(f'wait for {delay} sec...')
                    await asyncio.sleep(delay)
                else:
                    raise RuntimeError('failed to approve')
            
            tx_call = self.contract.functions.deposit(karak_contract_address, value, int(value*0.99))
            
            logger.debug(f'{self.web3.from_wei(value, "ether"):.4f} {symbol} -> Karak')
            tx = await self.build_transaction(account, tx_call, 0)
            return await self.send_and_wait_for_transaction(account, tx)

    def _get_value(self, balance):
        _max_value = float(self.web3.from_wei(balance, 'ether'))
        if not self.config['amount_percent']:
            value = random_float(self.config['amount'][0],
                                 min(self.config['amount'][1], _max_value))
        else:
            if self.config['amount_percent'][0] == self.config['amount_percent'][1] == 100:
                return balance
            value = _max_value * random.randint(*self.config['amount_percent']) / 100.0
        return self.web3.to_wei(value, 'ether')

    def _get_headers(self):
        ua = ua_generator.generate(device='desktop', browser=('chrome', 'safari'), platform=('windows', 'macos'))
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://app.karak.network',
            'Referer': 'https://app.karak.network/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'content-type': 'application/json',
        }
        headers.update(ua.headers.get())
        return headers

    def _save_referals(self, data, count):
        try:
            codes = [data['code'] for data in data[0]['result']['data']]
        except Exception as ex:
            logger.error(f'could not collect ref codes: {ex}')
            return
        codes = codes[:count]
        if not self.config.get('referal_codes_file'):
            return
        with open(self.config['referal_codes_file'], 'a') as fw:
            for code in codes:
                fw.write(f'{code}\n')

    async def _login_karak(self, account):
        headers = self._get_headers()
        ref = random.choice(['6vnaa', 'G8MAa', 'PD78C', 'rC1pA', 'Z02Xx', '6n3sK'])
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
            self._save_referals(response.json(), 1)
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
        json_data = {"0": {"referralCode": "%s" % ref}}

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

        params = {
            'batch': '1',
            'input': '{"0":{"wallet":"%s"}}' % account.address,
        }
        response = requests.get('https://restaking-backend.karak.network/getReferrals', params=params, headers=headers,
                                proxies=proxies)
        self._save_referals(response.json(), 1)

        logger.debug('wallet registered!')
