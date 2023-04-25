from web3 import Web3, HTTPProvider
import requests
from termcolor import cprint
from tabulate import tabulate


# ENTER YOUR WALLET HERE
WALLET = "0xbd6dbee69e43caec12c76bbe805750760cc70b0e"
# ENTER YOUR WALLET HERE


def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        eth_price = data["ethereum"]["usd"]
        return eth_price
    else:
        return None


def get_avax_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "AVAXUSDT"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        return None


def get_bnb_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "BNBUSDT"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        return None


def get_matic_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "MATICUSDT"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        return None


def get_fantom_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "FTMUSDT"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()["price"])
    else:
        return None


def check_token_balance(token_address, wallet_address, token_abi):
    contract = w3.eth.contract(address=token_address, abi=token_abi)
    balance = contract.functions.balanceOf(wallet_address).call()
    return balance


eth_native_networks = {
    "Ethereum": "https://rpc.ankr.com/eth",
    "Optimism": "https://opt-mainnet.g.alchemy.com/v2/demo",
    "Arbitrum One ": "https://arb1.arbitrum.io/rpc",
    "Arbitrum Nova": "https://nova.arbitrum.io/rpc",
    "zkSync": "https://mainnet.era.zksync.io",
    "AVAX": "https://api.avax.network/ext/bc/C/rpc",
    "BSC": "https://bsc-dataseed.binance.org",
    "Polygon": "https://polygon-rpc.com",
    "Fantom": "https://rpc.ankr.com/fantom",
}


results = []
wallet_gas_summ = 0

for network_name, rpc in eth_native_networks.items():
    w3 = Web3(HTTPProvider(rpc))
    ETH_balance = w3.from_wei(
        w3.eth.get_balance(w3.to_checksum_address(WALLET)), "ether"
    )

    if network_name == "AVAX":
        ticker = "AVAX"
        price = get_avax_price()
    elif network_name == "BSC":
        ticker = "BNB"
        price = get_bnb_price()
    elif network_name == "Polygon":
        ticker = "MATIC"
        price = get_matic_price()
    elif network_name == "Fantom":
        ticker = "FTM"
        price = get_fantom_price()
    else:
        ticker = "ETH"
        price = get_eth_price()

    results.append(
        [
            network_name,
            round(ETH_balance, 5),
            ticker,
            f"{round(float(ETH_balance) * float(price), 2)}$",
        ]
    )
    wallet_gas_summ += float(ETH_balance) * float(price)

cprint(tabulate(results, headers=["Network", "Balance", "Ticker", "Price"]), "white")
cprint(f"\nSUMM IN GAS: {round(wallet_gas_summ, 2)}$", "white")
