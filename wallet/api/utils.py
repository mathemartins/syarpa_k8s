import json
import os
import requests

from rest_framework import status
from rest_framework.response import Response
from time import sleep
from web3 import Web3

from wallet.abis.usdt import erc20_usdt_abi, bep20_usdt_abi
from wallet.models import Ethereum, TetherUSD, BinanceCoin, TetherUSDBEP20


class EtherChain:
    def __init__(self, infura_endpoint=os.environ.get('INFURA_ENDPOINT')):
        self.infura_endpoint = infura_endpoint

    def create_wallet(self):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            return web3.eth.account.create()
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_gas_price(self):
        import requests
        url = "https://ethgasstation.info/api/ethgasAPI.json?api-key" \
              "=3d8d6fc803ee423ffe629e5d50689a72da4b67c2b975fe058f9e2bd11020 "
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_gas_price_web3(self):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            return web3.eth.gas_price
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_wallet_balance(self, address: str):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            balance = web3.eth.get_balance(address)
            return web3.fromWei(balance, 'ether')

    def get_trx_information(self, trx_hash):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            return web3.eth.get_transaction(transaction_hash=trx_hash)

    def send_ether(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            sender_obj = Ethereum.objects.get(uuid=uuid)
            gas_price = float(self.get_gas_price().get("fast")) / 10
            dc_private_key = web3.eth.account.decrypt(
                keyfile_json=sender_obj.encrypted_private_key,
                password=sender_obj.uuid
            )
            nonce = web3.eth.getTransactionCount(sender_obj.public_key)
            tx = {
                'nonce': nonce,
                'to': recipient_address,
                'value': web3.toWei(amount, 'ether'),
                'gas': 21000,
                'gasPrice': web3.toWei('{gasPrice}'.format(gasPrice=gas_price), 'gwei')
            }
            signed_transaction = web3.eth.account.signTransaction(
                tx, dc_private_key
            )
            tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            # waits for 10 seconds before updating balance
            sleep(10)

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )
        return Response({"message": "You are not connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def send_usdt(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            sender_obj = TetherUSD.objects.get(uuid=uuid)
            gas_price = float(self.get_gas_price().get("fast")) / 10
            dc_private_key = web3.eth.account.decrypt(
                keyfile_json=sender_obj.encrypted_private_key,
                password=sender_obj.uuid
            )
            usdt_contract_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
            usdt_contract_abi = json.loads(erc20_usdt_abi)
            usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)
            sender_address = Web3.toChecksumAddress(sender_obj.public_key)

            nonce = web3.eth.getTransactionCount(sender_address)
            tx = usdt_contract.functions.transfer(recipient_address, web3.toWei(amount, 'ether')).buildTransaction({
                'gas': 21000,
                'gasPrice': web3.toWei('{gasPrice}'.format(gasPrice=gas_price), 'gwei'),
                'nonce': nonce
            })
            signed_tx = web3.eth.account.signTransaction(tx, private_key=dc_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            # waits for 10 seconds before updating balance
            sleep(10)

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )

        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_usdt_balance(self, address: str):
        web3 = Web3(Web3.HTTPProvider(self.infura_endpoint))
        if web3.isConnected():
            usdt_contract_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
            usdt_contract_abi = json.loads(erc20_usdt_abi)
            usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)
            usdt_address = Web3.toChecksumAddress(address)
            usdt_balance = usdt_contract.functions.balanceOf(usdt_address).call()
            return web3.fromWei(usdt_balance, 'ether')


class BinanceSmartChain:
    def __init__(self, bsc_endpoint=os.environ.get('BINANCE_SMARTCHAIN')):
        self.bsc_endpoint = bsc_endpoint

    def create_wallet(self):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            return web3.eth.account.create()
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_gas_price(self):
        import requests
        url = "https://ethgasstation.info/api/ethgasAPI.json?api-key" \
              "=3d8d6fc803ee423ffe629e5d50689a72da4b67c2b975fe058f9e2bd11020 "
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_gas_price_web3(self):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            return web3.eth.gas_price
        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_wallet_balance(self, address: str):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            balance = web3.eth.get_balance(address)
            return web3.fromWei(balance, 'ether')

    def get_trx_information(self, trx_hash):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            return web3.eth.get_transaction(transaction_hash=trx_hash)

    def send_bnb(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            sender_obj = BinanceCoin.objects.get(uuid=uuid)
            gas_price = float(self.get_gas_price().get("fast")) / 10
            dc_private_key = web3.eth.account.decrypt(
                keyfile_json=sender_obj.encrypted_private_key,
                password=sender_obj.uuid
            )
            nonce = web3.eth.getTransactionCount(sender_obj.public_key)
            tx = {
                'nonce': nonce,
                'to': recipient_address,
                'value': web3.toWei(amount, 'ether'),
                'gas': 21000,
                'gasPrice': web3.toWei('{gasPrice}'.format(gasPrice=gas_price), 'gwei')
            }
            signed_transaction = web3.eth.account.signTransaction(
                tx, dc_private_key
            )
            tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            # waits for 10 seconds before updating balance
            sleep(10)

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )
        return Response({"message": "You are not connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def send_usdt(self, uuid: str, recipient_address: str, amount):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            sender_obj = TetherUSDBEP20.objects.get(uuid=uuid)
            gas_price = float(self.get_gas_price().get("fast")) / 10
            dc_private_key = web3.eth.account.decrypt(
                keyfile_json=sender_obj.encrypted_private_key,
                password=sender_obj.uuid
            )
            usdt_contract_address = Web3.toChecksumAddress('')
            usdt_contract_abi = json.loads(bep20_usdt_abi)
            usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)
            sender_address = Web3.toChecksumAddress(sender_obj.public_key)

            nonce = web3.eth.getTransactionCount(sender_address)
            tx = usdt_contract.functions.transfer(recipient_address, web3.toWei(amount, 'ether')).buildTransaction({
                'gas': 21000,
                'gasPrice': web3.toWei('{gasPrice}'.format(gasPrice=gas_price), 'gwei'),
                'nonce': nonce
            })
            signed_tx = web3.eth.account.signTransaction(tx, private_key=dc_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

            # waits for 10 seconds before updating balance
            sleep(10)

            return Response(
                {
                    'message': "transaction successful",
                    "tx_": web3.toHex(tx_hash),
                    "success": bool(web3.toHex(tx_hash))
                },
                status=status.HTTP_201_CREATED
            )

        return Response({"message": "You are connected to the blockchain"}, status=status.HTTP_400_BAD_REQUEST)

    def get_usdt_balance(self, address: str):
        web3 = Web3(Web3.HTTPProvider(self.bsc_endpoint))
        if web3.isConnected():
            usdt_contract_address = Web3.toChecksumAddress('')
            usdt_contract_abi = json.loads(bep20_usdt_abi)
            usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)
            usdt_address = Web3.toChecksumAddress(address)
            usdt_balance = usdt_contract.functions.balanceOf(usdt_address).call()
            return web3.fromWei(usdt_balance, 'ether')


class OminiChain:
    def __init__(
            self,
            tatum_api_key=os.environ.get('TATUM_API'),
            network_type=os.environ.get('TATUM_NETWORK_TYPE'),
            base_url=os.environ.get('TATUM_BASE_URL'),
    ):
        self.tatum_api_key = tatum_api_key
        self.network_type = network_type
        self.base_url = base_url

    def create_wallet(self):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': f'{self.tatum_api_key}',
        }
        params = {
            'type': f'{self.network_type}',
        }
        xpub_response = requests.get(f'{self.base_url}v3/bitcoin/wallet', headers=headers, params=params)
        xpub_response_dict: dict = json.loads(xpub_response.content.decode('utf-8'))
        address_response = requests.get(
            f'{self.base_url}v3/bitcoin/address/{xpub_response_dict.get("xpub")}/0',
            headers=headers, params=params
        )
        address_response_dict = json.loads(address_response.content.decode('utf-8'))
        json_data = {
            'index': 0,
            'mnemonic': f'{xpub_response_dict.get("mnemonic")}',
        }

        pk_response = requests.post(
            f'{self.base_url}/v3/bitcoin/wallet/priv', headers=headers, params=params,
            json=json_data
        )
        pk_response_dict: dict = json.loads(pk_response.content.decode('utf-8'))
        data = {
            "address": address_response_dict.get("address"),
            "mnemonic": xpub_response_dict.get("mnemonic"),
            "xpub": xpub_response_dict.get("xpub"),
            "private_key": pk_response_dict.get("key")
        }
        return Response(data=data, status=status.HTTP_200_OK)


api_key: str = os.environ.get("TATUM_API")
network: str = os.environ.get("TATUM_NETWORK_TYPE")

"""
Get Mnemonic seed phrase for user and coin
curl --request GET \
  --url 'https://api-eu1.tatum.io/v3/{coin}/wallet'.format(coin="litecoin") \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'

  curl --request GET \
  --url 'https://api-eu1.tatum.io/v3/ethereum/wallet' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'

  for ethereum 
  {"xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "mnemonic":"moral salmon pond clip artwork choice inject zoo measure bunker approve capital story deliver mask toward pumpkin crumble lava brand defense street smart near"}


  Response
  {"mnemonic":"snake village rifle perfect put twenty horn lemon victory shield eternal tired assume prosper frozen market syrup loyal retire panic inside snap rug nuclear",
  "xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8"}
"""


def get_mnemonic_seed_phrase(coin: str):
    headers = {'x-api-key': api_key}
    response = requests.get('https://api-eu1.tatum.io/v3/{coin}/wallet'.format(coin=coin), headers=headers)
    return response.json()


"""
Create Ledger Wallet for user and coin
curl --request POST \
  --url https://api-eu1.tatum.io/v3/ledger/account \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"currency":"ETH","xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "customer":{"accountingCurrency":"USD", "externalId": "62795458cf1a66a279592bbd"},
  "compliant":false,"accountingCurrency":"USD"}'


  for ethereum
  {"currency":"ETH","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},"frozen":false,
  "xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "accountingCurrency":"USD","customerId":"62795ff574ee9be5450db94b","id":"627966c5257a72ebe4df114f"}


  Response
  {"currency":"BTC","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},
  "frozen":false,"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "customerId":"62781ba7e9e4efcfd4e6c75c","accountingCurrency":"USD","id":"62781ba7e9e4efcfd4e6c75b"}
"""


def create_ledger_account(coin_symbol: str, xpub: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }

    json_data = {
        'currency': coin_symbol.upper(),
        'xpub': xpub,
        'customer': {'accountingCurrency': 'USD', 'externalId': '123654'},
        'compliant': False,
        'accountingCurrency': 'USD',
    }

    response = requests.post('https://api-eu1.tatum.io/v3/ledger/account', headers=headers, json=json_data)
    return response.json()


def create_ledger_account_for_added_coin(coin_symbol: str, xpub: str, ledger_id: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }

    customer_payload = {'accountingCurrency': 'USD', 'externalId': ledger_id}

    json_data = {
        'currency': coin_symbol.upper(),
        'xpub': xpub,
        'customer': customer_payload,
        'accountingCurrency': 'USD',
    }

    response = requests.post('https://api-eu1.tatum.io/v3/ledger/account', headers=headers, json=json_data)
    return response.json()


"""
Generate Deposit Address
curl --request POST \
  --url 'https://api-eu1.tatum.io/v3/offchain/account/627966c5257a72ebe4df114f/address' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'


  for ethereum
  {"xpub":"xpub6FFhTcsQeuLM3xhuMmtpH5t9m3hh1NRZJKJPUHe2Vx1gkrHH9pTJTrkwjYKcjVGExgmnzjex1u8foPEjoTRbpFrBu7Qh92zqTfxY2L2Jr6P",
  "derivationKey":1,"address":"0x04266ac3a846a4c5930dbaf3e364d4fc521ad457","currency":"ETH"}


  Response
  {"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "derivationKey":1,"address":"tb1q8mn5lseq7440uyzh52uk43kwtfvvm8ywxm2m2d","currency":"BTC"}%
"""


def get_address(ledger_id: str):
    headers = {'x-api-key': api_key}
    response = requests.post(
        'https://api-eu1.tatum.io/v3/offchain/account/{ledger_id}/address'.format(ledger_id=ledger_id),
        headers=headers
    )
    return response.json()


"""
Integrate Transaction Alert
curl --request POST \
  --url https://api-eu1.tatum.io/v3/subscription \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"type":"ADDRESS_TRANSACTION","attr":{"address":"tb1q8mn5lseq7440uyzh52uk43kwtfvvm8ywxm2m2d",
  "chain":"BTC","url":"https://webhook.tatum.io/account"}}'


  Response
  {"id":"62782eca15e52ab29ce7b02f"}
"""


def activate_transaction_alert(address: str, coin_symbol: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    json_data = {
        'type': 'ADDRESS_TRANSACTION',
        'attr': {
            'address': address,
            'chain': coin_symbol.upper(),
            'url': 'https://webhook.tatum.io/account',
        },
    }
    response = requests.post('https://api-eu1.tatum.io/v3/subscription', headers=headers, json=json_data)
    return response.json()


"""
List All Customers Account
curl --request GET \
  --url 'https://api-eu1.tatum.io/v3/ledger/account/customer/62795ff574ee9be5450db94b?pageSize=10' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'


  Response
  [{"currency":"BTC","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},
  "accountCode":null,"accountNumber":null,"frozen":false,
  "xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "customerId":"62781ba7e9e4efcfd4e6c75c","accountingCurrency":"USD","id":"62781ba7e9e4efcfd4e6c75b"}]
"""


def get_account_list(customer_id: str):
    headers = {'x-api-key': api_key}
    params = {'pageSize': '10'}
    response = requests.get(
        'https://api-eu1.tatum.io/v3/ledger/account/customer/{customer_id}'.format(customer_id=customer_id),
        params=params, headers=headers
    )
    return response.json()


"""
Last Transaction per account
curl --request POST \
  --url 'https://api-eu1.tatum.io/v3/ledger/transaction/customer?pageSize=10' \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"id":"62781ba7e9e4efcfd4e6c75c"}'

  Response
  []
"""


def get_last_transactions(customer_id: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    params = {'pageSize': '10'}

    json_data = {'id': customer_id}
    response = requests.post(
        'https://api-eu1.tatum.io/v3/ledger/transaction/customer',
        params=params, headers=headers, json=json_data
    )
    return response.json()


"""
Get Account Details
curl --request GET \
  --url https://api-eu1.tatum.io/v3/ledger/account/62781ba7e9e4efcfd4e6c75b \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'


  Response
  {"currency":"BTC","active":true,"balance":{"accountBalance":"0","availableBalance":"0"},
  "accountCode":null,"accountNumber":null,"frozen":false,
  "xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "customerId":"62781ba7e9e4efcfd4e6c75c","accountingCurrency":"USD","id":"62781ba7e9e4efcfd4e6c75b"}
"""


def get_account_details(ledger_id: str):
    headers = {'x-api-key': api_key}
    response = requests.get(
        'https://api-eu1.tatum.io/v3/ledger/account/{ledger_id}'.format(ledger_id=ledger_id),
        headers=headers
    )
    return response.json()


"""
Transactions connected to this account
curl --request POST \
  --url 'https://api-eu1.tatum.io/v3/ledger/transaction/account?pageSize=10' \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"id":"62781ba7e9e4efcfd4e6c75b"}'


  Response
  []
"""


def get_transactions_for_account(ledger_id: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    params = {'pageSize': '10'}
    json_data = {'id': ledger_id}
    response = requests.post(
        'https://api-eu1.tatum.io/v3/ledger/transaction/account',
        params=params, headers=headers, json=json_data
    )
    return response.json()


"""
Get all deposit address
curl --request GET \
  --url https://api-eu1.tatum.io/v3/offchain/account/62781ba7e9e4efcfd4e6c75b/address \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e'


  Response
  [{"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "derivationKey":1,"address":"tb1q8mn5lseq7440uyzh52uk43kwtfvvm8ywxm2m2d","currency":"BTC"},
  {"xpub":"tpubDFhQBEALpPC1svdY8FwinTRd9oEqojVgqpA8HQ9kPVz3zQPosuEZyPXmDmu9GrNAGzhTGeqJ1ca4f7M89HLnhMsWf1HAUdTtaAXryE2rHv8",
  "derivationKey":2,"address":"tb1qavdnz083xar0njnulgl6wnrpkzp0za064qumj3","currency":"BTC"}]
"""


def get_deposit_addresses(ledger_id: str):
    headers = {'x-api-key': api_key}
    response = requests.get(
        'https://api-eu1.tatum.io/v3/offchain/account/{ledger_id}/address'.format(ledger_id=ledger_id),
        headers=headers
    )
    return response.json()


"""
Transfer Asset
curl --request POST \
  --url https://api-eu1.tatum.io/v3/offchain/bitcoin/transfer \
  --header 'content-type: application/json' \
  --header 'x-api-key: 2e2468f5-d6d2-4e76-b364-02d25dc62e3e' \
  --data '{"senderAccountId":"5e68c66581f2ee32bc354087","address":"mpTwPdF8up9kidgcAStriUPwRdnE9MRAg7","amount":"0.001",
  "mnemonic":"urge pulp usage sister evidence arrest palm math please chief egg abuse",
  "xpub":"xpub6EsCk1uU6cJzqvP9CdsTiJwT2rF748YkPnhv5Qo8q44DG7nn2vbyt48YRsNSUYS44jFCW9gwvD9kLQu9AuqXpTpM1c5hgg9PsuBLdeNncid"}'


  Response
  {
      "id": "5e68c66581f2ee32bc354087",
      "txId": "c83f8818db43d9ba4accfe454aa44fc33123d47a4f89d47b314d6748eb0e9bc9",
      "completed": true
  }

"""


def transfer(coin: str, ledger_id: str, address: str, amount: str, seed_phrase: str, xpub: str):
    headers = {
        # 'content-type': 'application/json',
        'x-api-key': api_key,
    }
    json_data = {
        'senderAccountId': ledger_id,
        'address': address,
        'amount': amount,
        'mnemonic': seed_phrase,
        'xpub': xpub
    }
    response = requests.post(
        'https://api-eu1.tatum.io/v3/offchain/{coin}/transfer'.format(coin=coin),
        headers=headers, json=json_data
    )
    return response.json()
