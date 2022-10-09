import json
from web3 import Web3
import sys
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

#options = webdriver.ChromeOptions()
#options.binary_location = "/Applications/Opera"

# from dexscreener import *
# sys.path.append(os.path.abspath("/Users/andrew/Desktop/Skew Farming/dexscreener-0.2/dexscreener"))
# from client import *

Tokens = []

node = "https://arb-mainnet.g.alchemy.com/v2/UUN9USWFvBzXqqHc6R64DQrN4OQMTBjc"
Balancer3BTCPool = "0xc999678122cbf8a30cb72c53d4bdd72abd96af880001000000000000000000b4"
BalancerVaultAddress = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
BalancerVaultABI = [
    {
        "inputs": [
            {
                "internalType": "contract IAuthorizer",
                "name": "authorizer",
                "type": "address",
            },
            {"internalType": "contract IWETH", "name": "weth", "type": "address"},
            {
                "internalType": "uint256",
                "name": "pauseWindowDuration",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "bufferPeriodDuration",
                "type": "uint256",
            },
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "contract IAuthorizer",
                "name": "newAuthorizer",
                "type": "address",
            }
        ],
        "name": "AuthorizerChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "recipient",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
        ],
        "name": "ExternalBalanceTransfer",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "contract IFlashLoanRecipient",
                "name": "recipient",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "feeAmount",
                "type": "uint256",
            },
        ],
        "name": "FlashLoan",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "delta",
                "type": "int256",
            },
        ],
        "name": "InternalBalanceChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "bool", "name": "paused", "type": "bool"}
        ],
        "name": "PausedStateChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "liquidityProvider",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
            {
                "indexed": False,
                "internalType": "int256[]",
                "name": "deltas",
                "type": "int256[]",
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "protocolFeeAmounts",
                "type": "uint256[]",
            },
        ],
        "name": "PoolBalanceChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "assetManager",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "contract IERC20",
                "name": "token",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "cashDelta",
                "type": "int256",
            },
            {
                "indexed": False,
                "internalType": "int256",
                "name": "managedDelta",
                "type": "int256",
            },
        ],
        "name": "PoolBalanceManaged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "poolAddress",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "enum IVault.PoolSpecialization",
                "name": "specialization",
                "type": "uint8",
            },
        ],
        "name": "PoolRegistered",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "relayer",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "approved",
                "type": "bool",
            },
        ],
        "name": "RelayerApprovalChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32",
            },
            {
                "indexed": True,
                "internalType": "contract IERC20",
                "name": "tokenIn",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "contract IERC20",
                "name": "tokenOut",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256",
            },
        ],
        "name": "Swap",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
        ],
        "name": "TokensDeregistered",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "poolId",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
            {
                "indexed": False,
                "internalType": "address[]",
                "name": "assetManagers",
                "type": "address[]",
            },
        ],
        "name": "TokensRegistered",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "WETH",
        "outputs": [{"internalType": "contract IWETH", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "enum IVault.SwapKind", "name": "kind", "type": "uint8"},
            {
                "components": [
                    {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
                    {
                        "internalType": "uint256",
                        "name": "assetInIndex",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "assetOutIndex",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                ],
                "internalType": "struct IVault.BatchSwapStep[]",
                "name": "swaps",
                "type": "tuple[]",
            },
            {
                "internalType": "contract IAsset[]",
                "name": "assets",
                "type": "address[]",
            },
            {
                "components": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool",
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address",
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool",
                    },
                ],
                "internalType": "struct IVault.FundManagement",
                "name": "funds",
                "type": "tuple",
            },
            {"internalType": "int256[]", "name": "limits", "type": "int256[]"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        ],
        "name": "batchSwap",
        "outputs": [
            {"internalType": "int256[]", "name": "assetDeltas", "type": "int256[]"}
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
        ],
        "name": "deregisterTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "address payable", "name": "recipient", "type": "address"},
            {
                "components": [
                    {
                        "internalType": "contract IAsset[]",
                        "name": "assets",
                        "type": "address[]",
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "minAmountsOut",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool",
                    },
                ],
                "internalType": "struct IVault.ExitPoolRequest",
                "name": "request",
                "type": "tuple",
            },
        ],
        "name": "exitPool",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "contract IFlashLoanRecipient",
                "name": "recipient",
                "type": "address",
            },
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"},
            {"internalType": "bytes", "name": "userData", "type": "bytes"},
        ],
        "name": "flashLoan",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes4", "name": "selector", "type": "bytes4"}],
        "name": "getActionId",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getAuthorizer",
        "outputs": [
            {"internalType": "contract IAuthorizer", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getDomainSeparator",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
        ],
        "name": "getInternalBalance",
        "outputs": [
            {"internalType": "uint256[]", "name": "balances", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getNextNonce",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getPausedState",
        "outputs": [
            {"internalType": "bool", "name": "paused", "type": "bool"},
            {
                "internalType": "uint256",
                "name": "pauseWindowEndTime",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "bufferPeriodEndTime",
                "type": "uint256",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "poolId", "type": "bytes32"}],
        "name": "getPool",
        "outputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {
                "internalType": "enum IVault.PoolSpecialization",
                "name": "",
                "type": "uint8",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
            {"internalType": "contract IERC20", "name": "token", "type": "address"},
        ],
        "name": "getPoolTokenInfo",
        "outputs": [
            {"internalType": "uint256", "name": "cash", "type": "uint256"},
            {"internalType": "uint256", "name": "managed", "type": "uint256"},
            {"internalType": "uint256", "name": "lastChangeBlock", "type": "uint256"},
            {"internalType": "address", "name": "assetManager", "type": "address"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "poolId", "type": "bytes32"}],
        "name": "getPoolTokens",
        "outputs": [
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
            {"internalType": "uint256[]", "name": "balances", "type": "uint256[]"},
            {"internalType": "uint256", "name": "lastChangeBlock", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getProtocolFeesCollector",
        "outputs": [
            {
                "internalType": "contract ProtocolFeesCollector",
                "name": "",
                "type": "address",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "address", "name": "relayer", "type": "address"},
        ],
        "name": "hasApprovedRelayer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {
                "components": [
                    {
                        "internalType": "contract IAsset[]",
                        "name": "assets",
                        "type": "address[]",
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "maxAmountsIn",
                        "type": "uint256[]",
                    },
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool",
                    },
                ],
                "internalType": "struct IVault.JoinPoolRequest",
                "name": "request",
                "type": "tuple",
            },
        ],
        "name": "joinPool",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "enum IVault.PoolBalanceOpKind",
                        "name": "kind",
                        "type": "uint8",
                    },
                    {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
                    {
                        "internalType": "contract IERC20",
                        "name": "token",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                ],
                "internalType": "struct IVault.PoolBalanceOp[]",
                "name": "ops",
                "type": "tuple[]",
            }
        ],
        "name": "managePoolBalance",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "enum IVault.UserBalanceOpKind",
                        "name": "kind",
                        "type": "uint8",
                    },
                    {
                        "internalType": "contract IAsset",
                        "name": "asset",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address",
                    },
                ],
                "internalType": "struct IVault.UserBalanceOp[]",
                "name": "ops",
                "type": "tuple[]",
            }
        ],
        "name": "manageUserBalance",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "enum IVault.SwapKind", "name": "kind", "type": "uint8"},
            {
                "components": [
                    {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
                    {
                        "internalType": "uint256",
                        "name": "assetInIndex",
                        "type": "uint256",
                    },
                    {
                        "internalType": "uint256",
                        "name": "assetOutIndex",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                ],
                "internalType": "struct IVault.BatchSwapStep[]",
                "name": "swaps",
                "type": "tuple[]",
            },
            {
                "internalType": "contract IAsset[]",
                "name": "assets",
                "type": "address[]",
            },
            {
                "components": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool",
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address",
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool",
                    },
                ],
                "internalType": "struct IVault.FundManagement",
                "name": "funds",
                "type": "tuple",
            },
        ],
        "name": "queryBatchSwap",
        "outputs": [{"internalType": "int256[]", "name": "", "type": "int256[]"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "enum IVault.PoolSpecialization",
                "name": "specialization",
                "type": "uint8",
            }
        ],
        "name": "registerPool",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
            {
                "internalType": "contract IERC20[]",
                "name": "tokens",
                "type": "address[]",
            },
            {"internalType": "address[]", "name": "assetManagers", "type": "address[]"},
        ],
        "name": "registerTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "contract IAuthorizer",
                "name": "newAuthorizer",
                "type": "address",
            }
        ],
        "name": "setAuthorizer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bool", "name": "paused", "type": "bool"}],
        "name": "setPaused",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "address", "name": "relayer", "type": "address"},
            {"internalType": "bool", "name": "approved", "type": "bool"},
        ],
        "name": "setRelayerApproval",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "poolId", "type": "bytes32"},
                    {
                        "internalType": "enum IVault.SwapKind",
                        "name": "kind",
                        "type": "uint8",
                    },
                    {
                        "internalType": "contract IAsset",
                        "name": "assetIn",
                        "type": "address",
                    },
                    {
                        "internalType": "contract IAsset",
                        "name": "assetOut",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "bytes", "name": "userData", "type": "bytes"},
                ],
                "internalType": "struct IVault.SingleSwap",
                "name": "singleSwap",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "address", "name": "sender", "type": "address"},
                    {
                        "internalType": "bool",
                        "name": "fromInternalBalance",
                        "type": "bool",
                    },
                    {
                        "internalType": "address payable",
                        "name": "recipient",
                        "type": "address",
                    },
                    {
                        "internalType": "bool",
                        "name": "toInternalBalance",
                        "type": "bool",
                    },
                ],
                "internalType": "struct IVault.FundManagement",
                "name": "funds",
                "type": "tuple",
            },
            {"internalType": "uint256", "name": "limit", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
        ],
        "name": "swap",
        "outputs": [
            {"internalType": "uint256", "name": "amountCalculated", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {"stateMutability": "payable", "type": "receive"},
]


web3 = Web3(Web3.HTTPProvider(node))
contract = web3.eth.contract(address=BalancerVaultAddress, abi=BalancerVaultABI)

for i in contract.functions.getPoolTokens(Balancer3BTCPool).call()[0]:
    Tokens.append({"Address": i})
x = 0

for i in contract.functions.getPoolTokens(Balancer3BTCPool).call()[1]:
    Tokens[x].update({"Balance": i})
    x += 1

print(contract.functions.getPoolTokens(Balancer3BTCPool).call()[1][1])
